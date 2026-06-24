from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from datasets import RemoteSensingSample, build_eurosat_protocol
from degradations import apply_degradation
from memory import PatchCoreMemoryBank
from models import WideResNetPatchCoreBackbone
from utils.config import load_config
from utils.metrics import binary_auc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate exact vs approximate retrieval for EuroSAT-Hard DRA-Inspect runs."
    )
    parser.add_argument("--config", default="configs/patchcore_remote_sensing.yaml")
    parser.add_argument(
        "--ratio_dir",
        action="append",
        default=[],
        help="Optional mapping in the form ratio=/absolute/or/relative/result_dir. Can be repeated.",
    )
    parser.add_argument(
        "--output_csv",
        default="outputs/remote_sensing/results/eurosat_hard_ann_retrieval_summary.csv",
    )
    parser.add_argument(
        "--output_md",
        default="outputs/remote_sensing/results/eurosat_hard_ann_retrieval_summary.md",
    )
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--max_test_images", type=int, default=0)
    parser.add_argument("--approx_num_centroids", type=int, default=256)
    parser.add_argument("--approx_nprobe", type=int, default=4)
    parser.add_argument("--approx_train_samples", type=int, default=20000)
    parser.add_argument("--approx_kmeans_iters", type=int, default=6)
    parser.add_argument("--approx_max_candidates", type=int, default=8192)
    return parser.parse_args()


def resolve_device(requested_device: str) -> str:
    if requested_device.startswith("cuda"):
        if torch.cuda.is_available():
            return requested_device
        print("Requested CUDA device is unavailable in the current environment. Falling back to CPU.")
        return "cpu"
    return requested_device


def maybe_degrade(image: Image.Image, degradation: str, severity: float) -> Image.Image:
    if degradation == "clean":
        return image.convert("RGB")
    return apply_degradation(image.convert("RGB"), name=degradation, severity=severity)


def image_score_from_patches(scores: np.ndarray, topk_ratio: float) -> float:
    k = max(1, int(round(len(scores) * topk_ratio)))
    return float(np.mean(np.sort(scores)[-k:]))


def fixed_operating_metrics(labels: np.ndarray, scores: np.ndarray, threshold: float) -> dict[str, float]:
    predictions = scores > threshold
    positive = labels == 1
    negative = labels == 0
    tp = int(np.sum(predictions & positive))
    fp = int(np.sum(predictions & negative))
    tn = int(np.sum((~predictions) & negative))
    fn = int(np.sum((~predictions) & positive))
    tpr = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    f1 = float(2 * precision * tpr / (precision + tpr)) if (precision + tpr) > 0 else 0.0
    bacc = float(0.5 * (tpr + (1.0 - fpr)))
    return {
        "fpr": fpr,
        "tpr": tpr,
        "f1": f1,
        "bacc": bacc,
    }


def split_train_normal(
    samples: list[RemoteSensingSample],
    split_ratio: float,
    seed: int,
) -> tuple[list[RemoteSensingSample], list[RemoteSensingSample]]:
    if len(samples) < 2:
        raise ValueError("Need at least 2 normal training samples for memory/calibration split.")
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(samples))
    calibration_count = int(round(len(samples) * split_ratio))
    calibration_count = min(max(1, calibration_count), len(samples) - 1)
    calibration_indices = set(order[:calibration_count].tolist())
    calibration_samples = [sample for idx, sample in enumerate(samples) if idx in calibration_indices]
    memory_samples = [sample for idx, sample in enumerate(samples) if idx not in calibration_indices]
    return memory_samples, calibration_samples


def synchronize_if_needed(device: str) -> None:
    if device.startswith("cuda") and torch.cuda.is_available():
        torch.cuda.synchronize()


def score_one_image(
    image: Image.Image,
    degradation: str,
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
    retrieval_backend: str,
    approx_kwargs: dict[str, int],
) -> float:
    scored_image = maybe_degrade(image, degradation, severity)
    output = backbone.extract(scored_image)
    patch_scores = bank.nearest_distances(
        output.features,
        retrieval_backend=retrieval_backend,
        **approx_kwargs,
    )
    return image_score_from_patches(patch_scores, topk_ratio)


def score_samples(
    samples: list[RemoteSensingSample],
    degradation: str,
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
    retrieval_backend: str,
    approx_kwargs: dict[str, int],
    warmup: int = 0,
    measure_time: bool = False,
) -> tuple[np.ndarray, list[float]]:
    if warmup > 0:
        for sample in samples[: min(warmup, len(samples))]:
            image = Image.open(sample.image_path).convert("RGB")
            _ = score_one_image(
                image,
                degradation,
                severity,
                backbone,
                bank,
                topk_ratio,
                retrieval_backend,
                approx_kwargs,
            )

    scores: list[float] = []
    elapsed_ms: list[float] = []
    for sample in samples:
        image = Image.open(sample.image_path).convert("RGB")
        synchronize_if_needed(str(backbone.device))
        start = time.perf_counter()
        score = score_one_image(
            image,
            degradation,
            severity,
            backbone,
            bank,
            topk_ratio,
            retrieval_backend,
            approx_kwargs,
        )
        synchronize_if_needed(str(backbone.device))
        if measure_time:
            elapsed_ms.append((time.perf_counter() - start) * 1000.0)
        scores.append(score)
    return np.asarray(scores, dtype=np.float32), elapsed_ms


def score_samples_for_degradations(
    samples: list[RemoteSensingSample],
    degradations: list[str],
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
    retrieval_backend: str,
    approx_kwargs: dict[str, int],
) -> np.ndarray:
    all_scores = []
    for degradation in degradations:
        scores, _ = score_samples(
            samples,
            degradation,
            severity,
            backbone,
            bank,
            topk_ratio,
            retrieval_backend,
            approx_kwargs,
        )
        all_scores.append(scores)
    if not all_scores:
        return np.asarray([], dtype=np.float32)
    return np.concatenate(all_scores, axis=0)


def build_protocol_bundle(
    payload: dict,
    dataset_root: str,
    default_seed: int,
) -> dict[str, object]:
    max_anomaly = payload.get("anomaly_cap_per_class")
    max_anomaly = None if max_anomaly is None else int(max_anomaly)
    return build_eurosat_protocol(
        root=dataset_root,
        normal_class=str(payload["normal_class"]),
        seed=int(payload.get("seed", default_seed)),
        protocol=str(payload.get("protocol_name", "hard")),
        hard_protocol=payload.get("protocol_key"),
        train_ratio=float(payload["train_ratio"]),
        max_anomaly_test_samples_per_class=max_anomaly,
    )


def default_ratio_dirs() -> dict[str, Path]:
    base = REPO_ROOT / "outputs/remote_sensing/results"
    return {
        "0.10": base / "eurosat_hard_main",
        "0.02": base / "eurosat_hard_core002",
    }


def payload_float(payload: dict, key: str, fallback: float) -> float:
    value = payload.get(key, fallback)
    return float(value if value is not None else fallback)


def resolve_ratio_dirs(items: list[str]) -> dict[str, Path]:
    mapping = default_ratio_dirs()
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Invalid --ratio_dir value: {item}")
        ratio, raw_path = item.split("=", 1)
        path = Path(raw_path)
        if not path.is_absolute():
            path = REPO_ROOT / path
        mapping[ratio] = path
    return mapping


def select_payloads(result_dir: Path) -> list[dict]:
    payloads = []
    for json_path in sorted(result_dir.glob("*.json")):
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        if str(payload.get("dataset_name")) != "eurosat":
            continue
        if str(payload.get("base_memory_mode")) != "mixed":
            continue
        if "corruption_agnostic" not in list(payload.get("threshold_protocols", [])):
            continue
        payload["_json_path"] = str(json_path)
        payloads.append(payload)
    return payloads


def ratio_rows(
    *,
    ratio: str,
    result_dir: Path,
    dataset_root: str,
    default_seed: int,
    backbone: WideResNetPatchCoreBackbone,
    topk_ratio: float,
    approx_kwargs: dict[str, int],
    warmup: int,
    max_test_images: int,
) -> list[dict[str, float | str]]:
    payloads = select_payloads(result_dir)
    if not payloads:
        raise ValueError(f"No DRA mixed/calibrated payloads found in {result_dir}")

    bank_cache: dict[tuple[str, str], PatchCoreMemoryBank] = {}
    quantile_cache: dict[tuple[str, str], tuple[float, float]] = {}
    rows: list[dict[str, float | str]] = []

    for retrieval_backend in ("exact", "approx_ivf"):
        aucs: list[float] = []
        fprs: list[float] = []
        f1s: list[float] = []
        baccs: list[float] = []
        tprs: list[float] = []
        elapsed_ms: list[float] = []

        for payload in payloads:
            bundle = build_protocol_bundle(payload, dataset_root=dataset_root, default_seed=default_seed)
            train_samples = list(bundle["train_samples"])
            test_samples = list(bundle["test_samples"])
            _, calibration_samples = split_train_normal(
                train_samples,
                split_ratio=float(payload["calibration_split"]),
                seed=int(payload.get("seed", default_seed)),
            )
            if max_test_images > 0:
                test_samples = test_samples[:max_test_images]

            bank_path = str(REPO_ROOT / str(payload["memory_bank_path"]))
            cache_key = (bank_path, retrieval_backend)
            if cache_key not in bank_cache:
                bank = PatchCoreMemoryBank.load(bank_path, device=str(backbone.device))
                if retrieval_backend == "approx_ivf":
                    bank.build_approx_ivf_index(
                        num_centroids=int(approx_kwargs["num_centroids"]),
                        train_samples=int(approx_kwargs["train_samples"]),
                        kmeans_iters=int(approx_kwargs["kmeans_iters"]),
                    )
                bank_cache[cache_key] = bank
            bank = bank_cache[cache_key]

            quantile_key = (bank_path, retrieval_backend)
            if quantile_key not in quantile_cache:
                agnostic_degradations = list(
                    payload["calibration_stats"]["corruption_agnostic"]["calibration_degradations"]
                )
                calibration_scores = score_samples_for_degradations(
                    calibration_samples,
                    agnostic_degradations,
                payload_float(payload, "memory_severity", payload_float(payload, "severity", 1.0)),
                    backbone,
                    bank,
                    topk_ratio,
                    retrieval_backend,
                    approx_kwargs,
                )
                quantile_cache[quantile_key] = (
                    float(np.percentile(calibration_scores, 50)),
                    float(np.percentile(calibration_scores, 95)),
                )
            q50, q95 = quantile_cache[quantile_key]

            scores, timings = score_samples(
                test_samples,
                str(payload["degradation"]),
                payload_float(payload, "eval_severity", payload_float(payload, "severity", 1.0)),
                backbone,
                bank,
                topk_ratio,
                retrieval_backend,
                approx_kwargs,
                warmup=warmup,
                measure_time=True,
            )
            calibrated_scores = (scores - q50) / (q95 - q50 + 1e-8)
            labels = np.asarray([1 if sample.is_anomalous else 0 for sample in test_samples], dtype=int)
            metrics = fixed_operating_metrics(labels, calibrated_scores, 1.0)
            aucs.append(binary_auc(labels, calibrated_scores))
            fprs.append(metrics["fpr"])
            tprs.append(metrics["tpr"])
            f1s.append(metrics["f1"])
            baccs.append(metrics["bacc"])
            elapsed_ms.extend(timings)

        rows.append(
            {
                "ratio": ratio,
                "retrieval": "Exact" if retrieval_backend == "exact" else "Approx. IVF",
                "auc": float(np.mean(aucs)),
                "fpr": float(np.mean(fprs)),
                "tpr": float(np.mean(tprs)),
                "f1": float(np.mean(f1s)),
                "bacc": float(np.mean(baccs)),
                "avg_inference_ms": float(np.mean(elapsed_ms)),
            }
        )

    exact_ms = next(float(row["avg_inference_ms"]) for row in rows if row["retrieval"] == "Exact")
    for row in rows:
        row["speedup"] = float(exact_ms / float(row["avg_inference_ms"])) if row["avg_inference_ms"] else 0.0
    return rows


def build_markdown(df: pd.DataFrame, approx_kwargs: dict[str, int]) -> str:
    lines = ["# EuroSAT-Hard Approximate Retrieval Summary", ""]
    lines.append(
        "Approximate retrieval uses an IVF-style coarse-to-fine search on the same saved DRA memory bank, "
        "with recalibrated q50/q95 statistics under the approximate backend."
    )
    lines.append("")
    lines.append(
        f"- Approx. settings: nlist={approx_kwargs['num_centroids']}, "
        f"nprobe={approx_kwargs['nprobe']}, train_samples={approx_kwargs['train_samples']}, "
        f"kmeans_iters={approx_kwargs['kmeans_iters']}, max_candidates={approx_kwargs['max_candidates']}"
    )
    lines.append("")
    lines.append("| Ratio | Retrieval | AUROC | FPR | TPR | F1 | BAcc | ms/img | Speedup |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for _, row in df.iterrows():
        lines.append(
            f"| {row['ratio']} | {row['retrieval']} | {row['auc']:.4f} | {row['fpr']:.4f} | {row['tpr']:.4f} | "
            f"{row['f1']:.4f} | {row['bacc']:.4f} | {row['avg_inference_ms']:.2f} | {row['speedup']:.2f}x |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    patchcore_cfg = config["patchcore"]
    device = resolve_device(str(patchcore_cfg.get("device", "cpu")))
    topk_ratio = float(patchcore_cfg.get("topk_ratio", 0.1))
    default_seed = int(config.get("seed", 42))
    dataset_root = str(config["dataset"]["roots"]["eurosat"])

    backbone = WideResNetPatchCoreBackbone(
        image_size=int(config["feature_extractor"]["image_size"]),
        pretrained=bool(config["feature_extractor"].get("pretrained", True)),
        layers=tuple(config["feature_extractor"].get("layers", ["layer2", "layer3"])),
        device=device,
    )

    approx_kwargs = {
        "num_centroids": int(args.approx_num_centroids),
        "nprobe": int(args.approx_nprobe),
        "train_samples": int(args.approx_train_samples),
        "kmeans_iters": int(args.approx_kmeans_iters),
        "max_candidates": int(args.approx_max_candidates),
    }

    rows: list[dict[str, float | str]] = []
    for ratio, result_dir in sorted(resolve_ratio_dirs(args.ratio_dir).items(), key=lambda item: float(item[0]), reverse=True):
        rows.extend(
            ratio_rows(
                ratio=ratio,
                result_dir=result_dir,
                dataset_root=dataset_root,
                default_seed=default_seed,
                backbone=backbone,
                topk_ratio=topk_ratio,
                approx_kwargs=approx_kwargs,
                warmup=int(args.warmup),
                max_test_images=int(args.max_test_images),
            )
        )

    df = pd.DataFrame(rows)
    output_csv = REPO_ROOT / args.output_csv
    output_md = REPO_ROOT / args.output_md
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    output_md.write_text(build_markdown(df, approx_kwargs), encoding="utf-8")
    print(f"Saved: {output_csv}")
    print(f"Saved: {output_md}")


if __name__ == "__main__":
    main()
