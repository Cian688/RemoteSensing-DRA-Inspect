from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run PaDiM baseline on remote sensing one-class anomaly detection protocols."
    )
    parser.add_argument("--dataset", choices=["eurosat", "resisc45"], required=True)
    parser.add_argument("--normal_class", required=True, help="Normal scene class for one-class training.")
    parser.add_argument("--protocol", choices=["one_vs_rest", "hard"], default="one_vs_rest")
    parser.add_argument("--hard_anomalies", nargs="*", default=None)
    parser.add_argument("--hard_protocol", default=None)
    parser.add_argument("--degradation", required=True)
    parser.add_argument("--enable_calibration", action="store_true")
    parser.add_argument("--calibration_split", type=float, default=0.2)
    parser.add_argument(
        "--threshold_protocols",
        nargs="+",
        choices=["clean_fixed", "corruption_agnostic"],
        default=["clean_fixed", "corruption_agnostic"],
    )
    parser.add_argument("--train_ratio", type=float, default=None)
    parser.add_argument("--max_anomaly_test_samples_per_class", type=int, default=None)
    parser.add_argument("--config", default="configs/patchcore_remote_sensing.yaml")
    parser.add_argument("--output_dir", default="outputs/remote_sensing/results/padim_eurosat_hard")
    parser.add_argument("--gpu", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--padim_dim", type=int, default=256, help="Feature dimensions retained for PaDiM.")
    parser.add_argument("--padim_reg", type=float, default=0.01, help="Covariance regularization.")
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
from memory import PaDiMStatsModel
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


def safe_tag(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def score_image(
    image: Image.Image,
    degradation: str,
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    model: PaDiMStatsModel,
    topk_ratio: float,
) -> float:
    degraded_image = maybe_degrade(image, degradation, severity)
    output = backbone.extract(degraded_image)
    patch_scores = model.mahalanobis(output.features)
    return image_score_from_patches(patch_scores, topk_ratio=topk_ratio)


def score_samples(
    samples: list[RemoteSensingSample],
    degradation: str,
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    model: PaDiMStatsModel,
    topk_ratio: float,
) -> np.ndarray:
    scores = []
    for sample in tqdm(samples, desc=f"Scoring calibration samples ({degradation})", leave=False):
        image = Image.open(sample.image_path).convert("RGB")
        scores.append(score_image(image, degradation, severity, backbone, model, topk_ratio))
    return np.asarray(scores, dtype=np.float32)


def score_samples_for_degradations(
    samples: list[RemoteSensingSample],
    degradations: list[str],
    severity: float,
    backbone: WideResNetPatchCoreBackbone,
    model: PaDiMStatsModel,
    topk_ratio: float,
) -> np.ndarray:
    all_scores = []
    for degradation in degradations:
        all_scores.append(score_samples(samples, degradation, severity, backbone, model, topk_ratio))
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


def build_or_load_model(
    *,
    output_root: Path,
    dataset_name: str,
    normal_class: str,
    protocol_name: str,
    samples: list[RemoteSensingSample],
    backbone: WideResNetPatchCoreBackbone,
    seed: int,
    padim_dim: int,
    padim_reg: float,
) -> tuple[PaDiMStatsModel, Path]:
    cache_path = (
        output_root
        / "remote_sensing"
        / "padim_models"
        / (
            f"{dataset_name}__{safe_tag(normal_class)}__{protocol_name}"
            f"__dim{padim_dim}__reg{str(padim_reg).replace('.', 'p')}__seed{seed}.npz"
        )
    )
    if cache_path.exists():
        return PaDiMStatsModel.load(cache_path), cache_path

    model = PaDiMStatsModel(feature_dim_subsample=padim_dim, regularization=padim_reg, seed=seed)
    for sample in tqdm(samples, desc=f"Building PaDiM stats for {dataset_name}/{normal_class}"):
        image = Image.open(sample.image_path).convert("RGB")
        features = backbone.extract(image).features
        model.add(features)
    model.finalize()
    model.save(cache_path)
    return model, cache_path


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
    configured_degradations = list(
        degradation_cfg.get("degradations", ["noise", "blur", "light", "lowres", "jpeg"])
    )
    severity = float(degradation_cfg.get("severity", 1.0))
    seed = int(ARGS.seed if ARGS.seed is not None else config.get("seed", 42))
    topk_ratio = float(patchcore_cfg.get("topk_ratio", 0.1))
    device = resolve_device(str(patchcore_cfg.get("device", "cpu")))
    requested_protocols = list(dict.fromkeys(ARGS.threshold_protocols))
    if "clean_fixed" not in requested_protocols:
        requested_protocols = ["clean_fixed", *requested_protocols]
    print(f"Remote-sensing PaDiM device: {device}")
    print(f"Threshold protocols: {requested_protocols}")

    if not ARGS.enable_calibration and any(name != "clean_fixed" for name in requested_protocols):
        raise ValueError("Calibration must be enabled to evaluate corruption_agnostic.")

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

    model, model_path = build_or_load_model(
        output_root=output_root,
        dataset_name=ARGS.dataset,
        normal_class=str(protocol_bundle["normal_class"]),
        protocol_name=safe_tag(str(protocol_bundle.get("protocol_name", ARGS.protocol))),
        samples=memory_samples,
        backbone=backbone,
        seed=seed,
        padim_dim=ARGS.padim_dim,
        padim_reg=ARGS.padim_reg,
    )

    clean_calibration_scores = score_samples(
        calibration_samples, "clean", severity, backbone, model, topk_ratio
    )
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
    if ARGS.enable_calibration and "corruption_agnostic" in requested_protocols:
        agnostic_degradations = ["clean", *configured_degradations]
        agnostic_calibration_scores = score_samples_for_degradations(
            calibration_samples,
            agnostic_degradations,
            severity,
            backbone,
            model,
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
        raw_score = score_image(image, ARGS.degradation, severity, backbone, model, topk_ratio)
        protocol_scores = {"clean_fixed": float(raw_score)}
        for protocol_name, (q50, q95) in protocol_quantiles.items():
            protocol_scores[protocol_name] = float((raw_score - q50) / (q95 - q50 + eps))
        raw_labels.append(1 if sample.is_anomalous else 0)
        raw_scores.append(raw_score)
        for protocol_name, values in protocol_score_lists.items():
            values.append(protocol_scores[protocol_name])
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
                "image_score": float(protocol_scores.get("corruption_agnostic", raw_score)),
            }
        )

    labels = np.asarray(raw_labels, dtype=int)
    raw_scores_np = np.asarray(raw_scores, dtype=np.float32)
    raw_normal = raw_scores_np[labels == 0]
    raw_abnormal = raw_scores_np[labels == 1]
    protocol_metrics: dict[str, dict] = {}
    thresholds = {"clean_fixed_raw_q95": raw_threshold_clean_q95}

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

    payload = {
        "dataset_name": ARGS.dataset,
        "detector_name": "padim",
        "category": str(protocol_bundle["normal_class"]),
        "normal_class": str(protocol_bundle["normal_class"]),
        "scene_classes": list(protocol_bundle["scene_classes"]),
        "anomaly_classes": list(protocol_bundle["anomaly_classes"]),
        "anomaly_cap_per_class": protocol_bundle["anomaly_cap_per_class"],
        "protocol_name": ARGS.protocol,
        "protocol_key": protocol_bundle.get("protocol_name", ARGS.protocol),
        "degradation": ARGS.degradation,
        "memory_mode": "clean_calibrated" if ARGS.enable_calibration else "clean",
        "base_memory_mode": "clean",
        "enable_calibration": bool(ARGS.enable_calibration),
        "threshold_protocols": requested_protocols,
        "calibration_split": float(ARGS.calibration_split),
        "train_ratio": train_ratio,
        "severity": severity,
        "device": device,
        "padim_dim": int(ARGS.padim_dim),
        "padim_reg": float(ARGS.padim_reg),
        "num_memory_train_normal": len(memory_samples),
        "num_calibration_normal": len(calibration_samples),
        "num_test_samples": len(test_samples),
        "num_test_normal": int(np.sum(labels == 0)),
        "num_test_anomaly": int(np.sum(labels == 1)),
        "padim_model_path": str(model_path),
        "calibration_stats": calibration_stats,
        "thresholds": thresholds,
        "protocol_metrics": protocol_metrics,
        "raw_metrics": protocol_metrics["clean_fixed"],
        "calibrated_metrics": protocol_metrics.get("corruption_agnostic", protocol_metrics["clean_fixed"]),
        "samples": per_sample,
    }

    output_dir = ensure_dir(ARGS.output_dir)
    result_name = (
        f"{ARGS.dataset}_{safe_tag(str(protocol_bundle['normal_class']))}_"
        f"{safe_tag(str(protocol_bundle.get('protocol_name', ARGS.protocol)))}_"
        f"{ARGS.degradation}_padim_{'cal' if ARGS.enable_calibration else 'raw'}.json"
    )
    result_path = output_dir / result_name
    write_json(result_path, payload)
    print(
        f"[RS-PaDiM] dataset={ARGS.dataset}, normal={protocol_bundle['normal_class']}, "
        f"degradation={ARGS.degradation}, clean_fixed_fpr="
        f"{payload['protocol_metrics']['clean_fixed']['fixed_threshold_fpr']:.4f}"
    )
    if "corruption_agnostic" in payload["protocol_metrics"]:
        print(
            f"[RS-PaDiM][agnostic] auc={payload['protocol_metrics']['corruption_agnostic']['image_auc']:.4f}, "
            f"fixed_fpr={payload['protocol_metrics']['corruption_agnostic']['fixed_threshold_fpr']:.4f}"
        )


if __name__ == "__main__":
    main()
