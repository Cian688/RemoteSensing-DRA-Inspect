from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run DRA-Inspect on remote sensing one-class anomaly detection protocols."
    )
    parser.add_argument("--dataset", choices=["eurosat", "resisc45"], required=True)
    parser.add_argument("--normal_class", required=True, help="Normal scene class for one-class training.")
    parser.add_argument(
        "--protocol",
        choices=["one_vs_rest", "hard"],
        default="one_vs_rest",
        help="Anomaly protocol for the remote sensing benchmark.",
    )
    parser.add_argument(
        "--hard_anomalies",
        nargs="*",
        default=None,
        help="Optional explicit hard-anomaly classes. If omitted, dataset defaults are used.",
    )
    parser.add_argument(
        "--hard_protocol",
        default=None,
        help="Named hard-anomaly protocol key for datasets that provide predefined pilot protocols.",
    )
    parser.add_argument("--degradation", required=True, help="Target test degradation.")
    parser.add_argument("--memory_mode", choices=["clean", "mixed"], default="mixed")
    parser.add_argument("--enable_calibration", action="store_true")
    parser.add_argument("--calibration_split", type=float, default=0.2)
    parser.add_argument("--calibration_method", choices=["quantile"], default="quantile")
    parser.add_argument(
        "--threshold_protocols",
        nargs="+",
        choices=["clean_fixed", "corruption_agnostic", "oracle"],
        default=["clean_fixed", "corruption_agnostic", "oracle"],
    )
    parser.add_argument("--train_ratio", type=float, default=None, help="Normal train/test split ratio.")
    parser.add_argument(
        "--max_anomaly_test_samples_per_class",
        type=int,
        default=None,
        help="Optional cap on anomaly test images per class.",
    )
    parser.add_argument(
        "--config",
        default="configs/patchcore_remote_sensing.yaml",
        help="YAML config path.",
    )
    parser.add_argument(
        "--output_dir",
        default="outputs/remote_sensing/results",
        help="Directory to store result JSON files.",
    )
    parser.add_argument("--gpu", default=None, help="Optional GPU id.")
    parser.add_argument("--seed", type=int, default=None, help="Optional seed override.")
    parser.add_argument(
        "--memory_severity",
        type=float,
        default=None,
        help="Optional severity override for mixed-memory construction and corruption-agnostic calibration.",
    )
    parser.add_argument(
        "--eval_severity",
        type=float,
        default=None,
        help="Optional severity override for degraded test-time evaluation.",
    )
    parser.add_argument(
        "--source_degradations",
        nargs="*",
        default=None,
        help="Optional explicit source degradations used for mixed-memory construction and agnostic calibration.",
    )
    parser.add_argument(
        "--coreset_sampling_ratio",
        type=float,
        default=None,
        help="Optional PatchCore coreset ratio override for this run.",
    )
    parser.add_argument(
        "--output_tag",
        default=None,
        help="Optional suffix tag appended to result filenames for multi-condition studies.",
    )
    return parser.parse_args()


ARGS = parse_args()
if ARGS.gpu is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = str(ARGS.gpu)

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import torch
from PIL import Image
from tqdm import tqdm

from datasets import RemoteSensingSample, build_eurosat_protocol, build_resisc45_protocol
from degradations import apply_degradation
from memory import PatchCoreMemoryBank
from models import WideResNetPatchCoreBackbone
from utils.config import load_config
from utils.io import ensure_dir, write_json
from utils.metrics import binary_auc


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


def summarize_distribution(normal_scores: np.ndarray, abnormal_scores: np.ndarray) -> dict:
    if len(normal_scores) == 0 or len(abnormal_scores) == 0:
        return {
            "normal_mean": 0.0,
            "normal_p95": 0.0,
            "abnormal_mean": 0.0,
            "gap": 0.0,
            "false_alarm_proxy": 0.0,
        }
    abnormal_median = float(np.median(abnormal_scores))
    return {
        "normal_mean": float(normal_scores.mean()),
        "normal_p95": float(np.percentile(normal_scores, 95)),
        "abnormal_mean": float(abnormal_scores.mean()),
        "gap": float(abnormal_scores.mean() - normal_scores.mean()),
        "false_alarm_proxy": float((normal_scores >= abnormal_median).mean()),
    }


def fixed_operating_metrics(labels: np.ndarray, scores: np.ndarray, threshold: float) -> dict:
    predictions = scores > threshold
    positive = labels == 1
    negative = labels == 0

    tp = int(np.sum(predictions & positive))
    fp = int(np.sum(predictions & negative))
    tn = int(np.sum((~predictions) & negative))
    fn = int(np.sum((~predictions) & positive))

    tpr = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    fnr = float(fn / (tp + fn)) if (tp + fn) > 0 else 0.0
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    f1 = float(2 * precision * tpr / (precision + tpr)) if (precision + tpr) > 0 else 0.0
    balanced_accuracy = float(0.5 * (tpr + (1.0 - fpr)))
    return {
        "fixed_threshold_fpr": fpr,
        "fixed_threshold_tpr": tpr,
        "fixed_threshold_fnr": fnr,
        "fixed_threshold_precision": precision,
        "fixed_threshold_f1": f1,
        "fixed_threshold_balanced_acc": balanced_accuracy,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
    }


def split_train_normal(
    samples: list[RemoteSensingSample], split_ratio: float, seed: int
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


def mixed_source_degradations(configured_degradations: list[str]) -> list[str]:
    merged = ["clean", *configured_degradations]
    seen = set()
    ordered = []
    for name in merged:
        if name not in seen:
            ordered.append(name)
            seen.add(name)
    return ordered


def source_degradations_for_mode(memory_mode: str, configured_degradations: list[str]) -> list[str]:
    if memory_mode == "clean":
        return ["clean"]
    if memory_mode == "mixed":
        return mixed_source_degradations(configured_degradations)
    raise ValueError(f"Unsupported memory mode: {memory_mode}")


def safe_tag(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def float_tag(value: float) -> str:
    return str(float(value)).replace(".", "p")


def build_or_load_bank(
    *,
    output_root: Path,
    dataset_name: str,
    normal_class: str,
    protocol_name: str,
    samples: list[RemoteSensingSample],
    source_degradations: list[str],
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    patchcore_cfg: dict,
    seed: int,
    device: str,
    calibration_split: float,
) -> tuple[PatchCoreMemoryBank, Path]:
    severity_tag = float_tag(severity)
    split_tag = str(calibration_split).replace(".", "p")
    source_tag = "-".join(source_degradations)
    coreset_tag = float_tag(float(patchcore_cfg.get("coreset_sampling_ratio", 0.1)))
    cache_path = (
        output_root
        / "remote_sensing"
        / "banks"
        / (
            f"{dataset_name}__{safe_tag(normal_class)}__{protocol_name}__{ARGS.memory_mode}"
            f"__src{source_tag}__split{split_tag}__sev{severity_tag}"
            f"__core{coreset_tag}__seed{seed}.npz"
        )
    )
    if cache_path.exists():
        return PatchCoreMemoryBank.load(cache_path, device=device), cache_path

    bank = PatchCoreMemoryBank(
        coreset_sampling_ratio=float(patchcore_cfg.get("coreset_sampling_ratio", 0.1)),
        nn_chunk_size=int(patchcore_cfg.get("nn_chunk_size", 2048)),
        seed=seed,
        device=device,
        max_bank_size=patchcore_cfg.get("max_bank_size"),
    )
    for sample in tqdm(samples, desc=f"Building bank for {dataset_name}/{normal_class}"):
        image = Image.open(sample.image_path).convert("RGB")
        for source_degradation in source_degradations:
            features = backbone.extract(maybe_degrade(image, source_degradation, severity)).features
            bank.add(features)
    bank.finalize()
    bank.save(cache_path)
    return bank, cache_path


def score_image(
    image: Image.Image,
    degradation: str,
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
) -> float:
    degraded_image = maybe_degrade(image, degradation, severity)
    output = backbone.extract(degraded_image)
    patch_scores = bank.nearest_distances(output.features)
    return image_score_from_patches(patch_scores, topk_ratio=topk_ratio)


def score_samples(
    samples: list[RemoteSensingSample],
    degradation: str,
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
) -> np.ndarray:
    scores = []
    for sample in tqdm(samples, desc=f"Scoring calibration samples ({degradation})", leave=False):
        image = Image.open(sample.image_path).convert("RGB")
        scores.append(score_image(image, degradation, severity, backbone, bank, topk_ratio))
    return np.asarray(scores, dtype=np.float32)


def score_samples_for_degradations(
    samples: list[RemoteSensingSample],
    degradations: list[str],
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    bank: PatchCoreMemoryBank,
    topk_ratio: float,
) -> np.ndarray:
    all_scores = []
    for degradation in degradations:
        all_scores.append(score_samples(samples, degradation, severity, backbone, bank, topk_ratio))
    if not all_scores:
        return np.asarray([], dtype=np.float32)
    return np.concatenate(all_scores, axis=0)


def build_protocol_samples(
    dataset_name: str,
    dataset_root: str,
    seed: int,
    train_ratio: float,
    max_anomaly_test_samples_per_class: int | None,
) -> dict[str, object]:
    if dataset_name == "eurosat":
        return build_eurosat_protocol(
            root=dataset_root,
            normal_class=ARGS.normal_class,
            seed=seed,
            protocol=ARGS.protocol,
            hard_protocol=ARGS.hard_protocol,
            train_ratio=train_ratio,
            anomaly_classes=ARGS.hard_anomalies,
            max_anomaly_test_samples_per_class=max_anomaly_test_samples_per_class,
        )
    if dataset_name == "resisc45":
        return build_resisc45_protocol(
            root=dataset_root,
            normal_class=ARGS.normal_class,
            seed=seed,
            protocol=ARGS.protocol,
            hard_protocol=ARGS.hard_protocol,
            train_ratio=train_ratio,
            anomaly_classes=ARGS.hard_anomalies,
            max_anomaly_test_samples_per_class=max_anomaly_test_samples_per_class,
        )
    raise ValueError(f"Unsupported remote sensing dataset: {dataset_name}")


def main() -> None:
    config = load_config(ARGS.config)
    output_root = Path(config["output"]["root"])
    dataset_root = config["dataset"]["roots"][ARGS.dataset]
    protocol_cfg = config["dataset"].get("protocol", {})
    train_ratio = float(ARGS.train_ratio if ARGS.train_ratio is not None else protocol_cfg.get("train_ratio", 0.8))
    max_anomaly_test_samples_per_class = ARGS.max_anomaly_test_samples_per_class
    if max_anomaly_test_samples_per_class is None:
        configured_limit = protocol_cfg.get("max_anomaly_test_samples_per_class")
        if configured_limit is not None:
            max_anomaly_test_samples_per_class = int(configured_limit)

    patchcore_cfg = config["patchcore"]
    degradation_cfg = config.get("degradation_eval", {})
    configured_degradations = list(degradation_cfg.get("degradations", ["noise", "blur", "light", "lowres", "jpeg"]))
    configured_source_degradations = (
        list(ARGS.source_degradations) if ARGS.source_degradations else configured_degradations
    )
    default_severity = float(degradation_cfg.get("severity", 1.0))
    memory_severity = float(ARGS.memory_severity if ARGS.memory_severity is not None else default_severity)
    eval_severity = float(ARGS.eval_severity if ARGS.eval_severity is not None else default_severity)
    seed = int(ARGS.seed if ARGS.seed is not None else config.get("seed", 42))
    patchcore_cfg = dict(patchcore_cfg)
    if ARGS.coreset_sampling_ratio is not None:
        patchcore_cfg["coreset_sampling_ratio"] = float(ARGS.coreset_sampling_ratio)
    topk_ratio = float(patchcore_cfg.get("topk_ratio", 0.1))
    device = resolve_device(str(patchcore_cfg.get("device", "cpu")))
    requested_protocols = list(dict.fromkeys(ARGS.threshold_protocols))
    if "clean_fixed" not in requested_protocols:
        requested_protocols = ["clean_fixed", *requested_protocols]
    print(f"Remote-sensing DRA device: {device}")
    print(f"Threshold protocols: {requested_protocols}")

    if not ARGS.enable_calibration and any(name != "clean_fixed" for name in requested_protocols):
        raise ValueError("Calibration must be enabled to evaluate corruption_agnostic or oracle protocols.")

    backbone = WideResNetPatchCoreBackbone(
        image_size=int(config["feature_extractor"]["image_size"]),
        pretrained=bool(config["feature_extractor"].get("pretrained", True)),
        layers=tuple(config["feature_extractor"].get("layers", ["layer2", "layer3"])),
        device=device,
    )

    protocol_bundle = build_protocol_samples(
        dataset_name=ARGS.dataset,
        dataset_root=dataset_root,
        seed=seed,
        train_ratio=train_ratio,
        max_anomaly_test_samples_per_class=max_anomaly_test_samples_per_class,
    )
    train_samples = list(protocol_bundle["train_samples"])
    test_samples = list(protocol_bundle["test_samples"])
    memory_samples, calibration_samples = split_train_normal(train_samples, ARGS.calibration_split, seed)
    source_degradations = source_degradations_for_mode(ARGS.memory_mode, configured_source_degradations)

    bank, bank_path = build_or_load_bank(
        output_root=output_root,
        dataset_name=ARGS.dataset,
        normal_class=str(protocol_bundle["normal_class"]),
        protocol_name=ARGS.protocol,
        samples=memory_samples,
        source_degradations=source_degradations,
        severity=memory_severity,
        backbone=backbone,
        patchcore_cfg=patchcore_cfg,
        seed=seed,
        device=device,
        calibration_split=ARGS.calibration_split,
    )

    clean_calibration_scores = score_samples(calibration_samples, "clean", memory_severity, backbone, bank, topk_ratio)
    raw_threshold_clean_q95 = float(np.percentile(clean_calibration_scores, 95))
    calibration_stats: dict[str, dict] = {
        "clean_fixed": {
            "score_space": "raw",
            "calibration_degradations": ["clean"],
            "q50_raw": float(np.percentile(clean_calibration_scores, 50)),
            "q95_raw": raw_threshold_clean_q95,
            "num_scores": int(clean_calibration_scores.shape[0]),
        }
    }

    protocol_quantiles: dict[str, tuple[float, float]] = {}
    if ARGS.enable_calibration and ARGS.calibration_method == "quantile":
        if "corruption_agnostic" in requested_protocols:
            agnostic_degradations = mixed_source_degradations(configured_source_degradations)
            agnostic_calibration_scores = score_samples_for_degradations(
                calibration_samples,
                agnostic_degradations,
                memory_severity,
                backbone,
                bank,
                topk_ratio,
            )
            agnostic_q50 = float(np.percentile(agnostic_calibration_scores, 50))
            agnostic_q95 = float(np.percentile(agnostic_calibration_scores, 95))
            protocol_quantiles["corruption_agnostic"] = (agnostic_q50, agnostic_q95)
            calibration_stats["corruption_agnostic"] = {
                "score_space": "calibrated",
                "calibration_degradations": agnostic_degradations,
                "q50_raw": agnostic_q50,
                "q95_raw": agnostic_q95,
                "num_scores": int(agnostic_calibration_scores.shape[0]),
            }
        if "oracle" in requested_protocols:
            oracle_calibration_scores = score_samples(
                calibration_samples, ARGS.degradation, eval_severity, backbone, bank, topk_ratio
            )
            oracle_q50 = float(np.percentile(oracle_calibration_scores, 50))
            oracle_q95 = float(np.percentile(oracle_calibration_scores, 95))
            protocol_quantiles["oracle"] = (oracle_q50, oracle_q95)
            calibration_stats["oracle"] = {
                "score_space": "calibrated",
                "calibration_degradations": [ARGS.degradation],
                "q50_raw": oracle_q50,
                "q95_raw": oracle_q95,
                "num_scores": int(oracle_calibration_scores.shape[0]),
            }

    eps = 1e-8
    raw_labels = []
    raw_scores = []
    protocol_score_lists: dict[str, list[float]] = {name: [] for name in requested_protocols if name != "clean_fixed"}
    per_sample = []

    for sample in tqdm(
        test_samples,
        desc=f"Evaluating {ARGS.dataset}/{protocol_bundle['normal_class']}/{ARGS.degradation}",
    ):
        image = Image.open(sample.image_path).convert("RGB")
        raw_score = score_image(image, ARGS.degradation, eval_severity, backbone, bank, topk_ratio)
        protocol_scores = {"clean_fixed": float(raw_score)}
        for protocol_name, (q50, q95) in protocol_quantiles.items():
            protocol_scores[protocol_name] = float((raw_score - q50) / (q95 - q50 + eps))
        raw_labels.append(1 if sample.is_anomalous else 0)
        raw_scores.append(raw_score)
        for protocol_name, values in protocol_score_lists.items():
            values.append(protocol_scores[protocol_name])
        default_calibrated_score = protocol_scores.get("corruption_agnostic", raw_score)
        per_sample.append(
            {
                "image_path": str(sample.image_path),
                "scene_label": sample.scene_label,
                "label": sample.label,
                "is_anomalous": bool(sample.is_anomalous),
                "normal_class": sample.normal_class,
                "protocol": sample.protocol,
                "raw_image_score": float(raw_score),
                "clean_fixed_image_score": float(raw_score),
                "corruption_agnostic_image_score": float(protocol_scores.get("corruption_agnostic", raw_score)),
                "oracle_image_score": float(protocol_scores.get("oracle", raw_score)),
                "calibrated_image_score": float(default_calibrated_score),
                "image_score": float(default_calibrated_score),
            }
        )

    labels = np.asarray(raw_labels, dtype=int)
    raw_scores_np = np.asarray(raw_scores, dtype=np.float32)
    raw_normal = raw_scores_np[labels == 0]
    raw_abnormal = raw_scores_np[labels == 1]
    protocol_metrics: dict[str, dict] = {}
    thresholds = {
        "clean_fixed_raw_q95": raw_threshold_clean_q95,
    }

    if "clean_fixed" in requested_protocols:
        protocol_metrics["clean_fixed"] = {
            "score_space": "raw",
            "threshold": raw_threshold_clean_q95,
            "image_auc": binary_auc(labels, raw_scores_np),
            **summarize_distribution(raw_normal, raw_abnormal),
            **fixed_operating_metrics(labels, raw_scores_np, raw_threshold_clean_q95),
        }

    for protocol_name, values in protocol_score_lists.items():
        scores_np = np.asarray(values, dtype=np.float32)
        normal_scores = scores_np[labels == 0]
        abnormal_scores = scores_np[labels == 1]
        thresholds[protocol_name] = 1.0
        protocol_metrics[protocol_name] = {
            "score_space": "calibrated",
            "threshold": 1.0,
            "image_auc": binary_auc(labels, scores_np),
            **summarize_distribution(normal_scores, abnormal_scores),
            **fixed_operating_metrics(labels, scores_np, 1.0),
        }

    default_calibrated_metrics = protocol_metrics.get(
        "corruption_agnostic",
        protocol_metrics.get("oracle", protocol_metrics["clean_fixed"]),
    )

    payload = {
        "dataset_name": ARGS.dataset,
        "category": str(protocol_bundle["normal_class"]),
        "normal_class": str(protocol_bundle["normal_class"]),
        "normal_classes": list(protocol_bundle.get("normal_classes", [protocol_bundle["normal_class"]])),
        "scene_classes": list(protocol_bundle["scene_classes"]),
        "anomaly_classes": list(protocol_bundle["anomaly_classes"]),
        "anomaly_cap_per_class": protocol_bundle["anomaly_cap_per_class"],
        "protocol_name": ARGS.protocol,
        "protocol_key": protocol_bundle.get("protocol_name", ARGS.protocol),
        "degradation": ARGS.degradation,
        "memory_mode": f"{ARGS.memory_mode}_calibrated" if ARGS.enable_calibration else ARGS.memory_mode,
        "base_memory_mode": ARGS.memory_mode,
        "enable_calibration": bool(ARGS.enable_calibration),
        "calibration_method": ARGS.calibration_method if ARGS.enable_calibration else None,
        "threshold_protocols": requested_protocols,
        "calibration_split": float(ARGS.calibration_split),
        "train_ratio": train_ratio,
        "seed": seed,
        "severity": default_severity,
        "memory_severity": memory_severity,
        "eval_severity": eval_severity,
        "coreset_sampling_ratio": float(patchcore_cfg.get("coreset_sampling_ratio", 0.1)),
        "source_degradations": source_degradations,
        "device": device,
        "num_memory_train_normal": len(memory_samples),
        "num_calibration_normal": len(calibration_samples),
        "num_test_samples": len(test_samples),
        "num_test_normal": int(np.sum(labels == 0)),
        "num_test_anomaly": int(np.sum(labels == 1)),
        "memory_bank_path": str(bank_path),
        "calibration_stats": calibration_stats,
        "thresholds": thresholds,
        "protocol_metrics": protocol_metrics,
        "raw_metrics": protocol_metrics["clean_fixed"],
        "calibrated_metrics": default_calibrated_metrics,
        "samples": per_sample,
    }

    output_dir = ensure_dir(ARGS.output_dir)
    suffix_parts = []
    if seed != int(config.get("seed", 42)):
        suffix_parts.append(f"seed{seed}")
    if abs(memory_severity - default_severity) > 1e-12:
        suffix_parts.append(f"memsev{float_tag(memory_severity)}")
    if abs(eval_severity - default_severity) > 1e-12:
        suffix_parts.append(f"evalsev{float_tag(eval_severity)}")
    if ARGS.coreset_sampling_ratio is not None:
        suffix_parts.append(f"core{float_tag(float(ARGS.coreset_sampling_ratio))}")
    if ARGS.source_degradations:
        suffix_parts.append("src" + "-".join(str(name) for name in source_degradations))
    if ARGS.output_tag:
        suffix_parts.append(safe_tag(str(ARGS.output_tag)))
    suffix = f"__{'__'.join(suffix_parts)}" if suffix_parts else ""
    result_name = (
        f"{ARGS.dataset}_{safe_tag(str(protocol_bundle['normal_class']))}_"
        f"{safe_tag(str(protocol_bundle.get('protocol_name', ARGS.protocol)))}_"
        f"{ARGS.degradation}_{ARGS.memory_mode}_{'cal' if ARGS.enable_calibration else 'raw'}{suffix}.json"
    )
    result_path = output_dir / result_name
    write_json(result_path, payload)
    print(
        f"[RS-DRA] dataset={ARGS.dataset}, normal={protocol_bundle['normal_class']}, "
        f"degradation={ARGS.degradation}, anomaly_cap={protocol_bundle['anomaly_cap_per_class']}, clean_fixed_fpr="
        f"{payload['protocol_metrics']['clean_fixed']['fixed_threshold_fpr']:.4f}"
    )
    if "corruption_agnostic" in payload["protocol_metrics"]:
        print(
            f"[RS-DRA][agnostic] auc={payload['protocol_metrics']['corruption_agnostic']['image_auc']:.4f}, "
            f"fixed_fpr={payload['protocol_metrics']['corruption_agnostic']['fixed_threshold_fpr']:.4f}"
        )
    if "oracle" in payload["protocol_metrics"]:
        print(
            f"[RS-DRA][oracle] auc={payload['protocol_metrics']['oracle']['image_auc']:.4f}, "
            f"fixed_fpr={payload['protocol_metrics']['oracle']['fixed_threshold_fpr']:.4f}"
        )


if __name__ == "__main__":
    main()
