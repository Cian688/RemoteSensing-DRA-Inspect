from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from datasets import build_eurosat_protocol, build_resisc45_protocol
from degradations import apply_degradation
from memory import PatchCoreMemoryBank
from models import WideResNetPatchCoreBackbone
from utils.config import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile runtime and memory-bank size for remote sensing PatchCore and DRA-Inspect."
    )
    parser.add_argument("--config", default="configs/patchcore_remote_sensing.yaml")
    parser.add_argument(
        "--eurosat_result_dir",
        default="outputs/remote_sensing/results/eurosat_hard_main",
    )
    parser.add_argument(
        "--resisc45_result_dir",
        default="outputs/remote_sensing/results/resisc45_hard_minimal",
    )
    parser.add_argument(
        "--output_csv",
        default="outputs/remote_sensing/results/runtime_memory_profile_remote_sensing.csv",
    )
    parser.add_argument(
        "--output_md",
        default="outputs/remote_sensing/results/runtime_memory_profile_remote_sensing.md",
    )
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--max_test_images", type=int, default=100)
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


def synchronize_if_needed(device: str) -> None:
    if device.startswith("cuda") and torch.cuda.is_available():
        torch.cuda.synchronize()


def reset_peak_memory_if_needed(device: str) -> None:
    if device.startswith("cuda") and torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()


def peak_memory_mb(device: str) -> float:
    if device.startswith("cuda") and torch.cuda.is_available():
        return float(torch.cuda.max_memory_allocated() / (1024 ** 2))
    return 0.0


def image_score_from_patches(scores: np.ndarray, topk_ratio: float) -> float:
    k = max(1, int(round(len(scores) * topk_ratio)))
    return float(np.mean(np.sort(scores)[-k:]))


def score_one_image(
    image: Image.Image,
    degradation: str,
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
) -> float:
    profiled_image = maybe_degrade(image, degradation, severity)
    output = backbone.extract(profiled_image)
    patch_scores = bank.nearest_distances(output.features)
    return image_score_from_patches(patch_scores, topk_ratio)


def bank_stats(bank: PatchCoreMemoryBank) -> tuple[int, int, float]:
    if bank.bank is None:
        raise ValueError("PatchCore memory bank is empty.")
    num_vectors = int(bank.bank.shape[0])
    dim = int(bank.bank.shape[1]) if bank.bank.ndim == 2 else 0
    memory_mb = float(bank.bank.nbytes / (1024 ** 2))
    return num_vectors, dim, memory_mb


def cycle_degradations(degradations: list[str], count: int) -> list[str]:
    if not degradations:
        degradations = ["clean"]
    return [degradations[idx % len(degradations)] for idx in range(count)]


def profile_inference(
    image_paths: list[Path],
    degradation_sequence: list[str],
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
    warmup: int,
    device: str,
) -> dict[str, float]:
    if not image_paths:
        raise ValueError("No test images available for profiling.")
    if len(image_paths) != len(degradation_sequence):
        raise ValueError("Degradation sequence length must match the profiled image count.")

    warmup_paths = image_paths[: min(warmup, len(image_paths))]
    warmup_degradations = degradation_sequence[: len(warmup_paths)]
    for image_path, degradation in zip(warmup_paths, warmup_degradations):
        image = Image.open(image_path).convert("RGB")
        _ = score_one_image(image, degradation, severity, backbone, bank, topk_ratio)

    synchronize_if_needed(device)
    reset_peak_memory_if_needed(device)

    elapsed_ms: list[float] = []
    for image_path, degradation in zip(image_paths, degradation_sequence):
        image = Image.open(image_path).convert("RGB")
        synchronize_if_needed(device)
        start = time.perf_counter()
        _ = score_one_image(image, degradation, severity, backbone, bank, topk_ratio)
        synchronize_if_needed(device)
        elapsed_ms.append((time.perf_counter() - start) * 1000.0)

    elapsed = np.asarray(elapsed_ms, dtype=np.float64)
    return {
        "num_test_images": float(len(image_paths)),
        "avg_inference_ms": float(elapsed.mean()),
        "p50_inference_ms": float(np.percentile(elapsed, 50)),
        "p95_inference_ms": float(np.percentile(elapsed, 95)),
        "peak_cuda_mem_mb": peak_memory_mb(device),
    }


def select_representative_payloads(result_dir: Path) -> list[dict]:
    by_key: dict[tuple[str, str], dict] = {}
    for json_path in sorted(result_dir.glob("*.json")):
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        base_memory_mode = str(payload.get("base_memory_mode", ""))
        protocol_key = str(payload.get("protocol_key", payload.get("protocol_name", "")))
        key = (protocol_key, base_memory_mode)
        if key not in by_key:
            payload["_json_path"] = str(json_path)
            by_key[key] = payload
    return list(by_key.values())


def collect_profile_degradations(result_dir: Path) -> list[str]:
    degradations = []
    for json_path in sorted(result_dir.glob("*.json")):
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        degradation = str(payload.get("degradation", "clean"))
        if degradation not in degradations:
            degradations.append(degradation)
    return degradations


def build_protocol_bundle(dataset_name: str, dataset_root: str, payload: dict, seed: int) -> dict[str, object]:
    protocol = str(payload.get("protocol_name", "hard"))
    train_ratio = float(payload.get("train_ratio", 0.8))
    max_anomaly = payload.get("anomaly_cap_per_class")
    max_anomaly = None if max_anomaly is None else int(max_anomaly)
    normal_class = str(payload["normal_class"])
    hard_protocol = payload.get("protocol_key") if protocol == "hard" else None

    if dataset_name == "eurosat":
        return build_eurosat_protocol(
            root=dataset_root,
            normal_class=normal_class,
            seed=seed,
            protocol=protocol,
            hard_protocol=hard_protocol,
            train_ratio=train_ratio,
            max_anomaly_test_samples_per_class=max_anomaly,
        )
    if dataset_name == "resisc45":
        return build_resisc45_protocol(
            root=dataset_root,
            normal_class=normal_class,
            seed=seed,
            protocol=protocol,
            hard_protocol=hard_protocol,
            train_ratio=train_ratio,
            max_anomaly_test_samples_per_class=max_anomaly,
        )
    raise ValueError(f"Unsupported dataset: {dataset_name}")


def profile_dataset(
    *,
    dataset_name: str,
    result_dir: Path,
    dataset_root: str,
    seed: int,
    backbone: WideResNetPatchCoreBackbone,
    topk_ratio: float,
    warmup: int,
    max_test_images: int,
    device: str,
) -> list[dict]:
    degradations = collect_profile_degradations(result_dir)
    payloads = select_representative_payloads(result_dir)
    rows: list[dict] = []
    for payload in payloads:
        bundle = build_protocol_bundle(dataset_name, dataset_root, payload, seed)
        test_samples = list(bundle["test_samples"])
        test_paths = [sample.image_path for sample in test_samples[:max_test_images]]
        degradation_sequence = cycle_degradations(degradations, len(test_paths))
        bank_path = REPO_ROOT / str(payload["memory_bank_path"])
        bank = PatchCoreMemoryBank.load(bank_path, device=device)
        profile = profile_inference(
            image_paths=test_paths,
            degradation_sequence=degradation_sequence,
            severity=float(payload.get("severity", 1.0)),
            backbone=backbone,
            bank=bank,
            topk_ratio=topk_ratio,
            warmup=warmup,
            device=device,
        )
        bank_vectors, bank_dim, bank_mb = bank_stats(bank)
        rows.append(
            {
                "dataset": dataset_name,
                "protocol_key": str(payload.get("protocol_key", payload.get("protocol_name", ""))),
                "method": "PatchCore" if str(payload.get("base_memory_mode")) == "clean" else "DRA-Inspect",
                "num_test_images": int(profile["num_test_images"]),
                "avg_inference_ms": profile["avg_inference_ms"],
                "p50_inference_ms": profile["p50_inference_ms"],
                "p95_inference_ms": profile["p95_inference_ms"],
                "peak_cuda_mem_mb": profile["peak_cuda_mem_mb"],
                "bank_vectors": bank_vectors,
                "bank_dim": bank_dim,
                "bank_mb": bank_mb,
                "extra_params": 0,
            }
        )
    return rows


def build_markdown(df: pd.DataFrame) -> str:
    lines = ["# Remote Sensing Runtime And Memory Profile", ""]
    lines.append("| Dataset | Method | Avg. ms/img | P50 ms | P95 ms | Peak GPU MB | Bank vectors | Bank MB | Extra params |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    grouped = (
        df.groupby(["dataset", "method"])[
            ["avg_inference_ms", "p50_inference_ms", "p95_inference_ms", "peak_cuda_mem_mb", "bank_vectors", "bank_mb", "extra_params"]
        ]
        .mean()
        .reset_index()
    )
    for _, row in grouped.iterrows():
        lines.append(
            f"| {row['dataset']} | {row['method']} | {row['avg_inference_ms']:.2f} | {row['p50_inference_ms']:.2f} | "
            f"{row['p95_inference_ms']:.2f} | {row['peak_cuda_mem_mb']:.2f} | {row['bank_vectors']:.1f} | "
            f"{row['bank_mb']:.2f} | {int(row['extra_params'])} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    patchcore_cfg = config["patchcore"]
    device = resolve_device(str(patchcore_cfg.get("device", "cpu")))
    seed = int(config.get("seed", 42))
    topk_ratio = float(patchcore_cfg.get("topk_ratio", 0.1))

    backbone = WideResNetPatchCoreBackbone(
        image_size=int(config["feature_extractor"]["image_size"]),
        pretrained=bool(config["feature_extractor"].get("pretrained", True)),
        layers=tuple(config["feature_extractor"].get("layers", ["layer2", "layer3"])),
        device=device,
    )

    rows = []
    rows.extend(
        profile_dataset(
            dataset_name="eurosat",
            result_dir=REPO_ROOT / args.eurosat_result_dir,
            dataset_root=config["dataset"]["roots"]["eurosat"],
            seed=seed,
            backbone=backbone,
            topk_ratio=topk_ratio,
            warmup=args.warmup,
            max_test_images=args.max_test_images,
            device=device,
        )
    )
    rows.extend(
        profile_dataset(
            dataset_name="resisc45",
            result_dir=REPO_ROOT / args.resisc45_result_dir,
            dataset_root=config["dataset"]["roots"]["resisc45"],
            seed=seed,
            backbone=backbone,
            topk_ratio=topk_ratio,
            warmup=args.warmup,
            max_test_images=args.max_test_images,
            device=device,
        )
    )

    df = pd.DataFrame(rows)
    output_csv = REPO_ROOT / args.output_csv
    output_md = REPO_ROOT / args.output_md
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    output_md.write_text(build_markdown(df), encoding="utf-8")
    print(f"Saved: {output_csv}")
    print(f"Saved: {output_md}")


if __name__ == "__main__":
    main()
