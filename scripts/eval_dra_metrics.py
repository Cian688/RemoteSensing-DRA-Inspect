from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, roc_auc_score, roc_curve


def load_scores(path: Path) -> tuple[dict, np.ndarray, np.ndarray]:
    data = json.loads(path.read_text(encoding="utf-8"))
    scores = []
    labels = []
    for sample in data.get("samples", []):
        score = sample.get("image_score", sample.get("score"))
        is_anom = sample.get("is_anomalous", sample.get("label", None))
        if isinstance(is_anom, str):
            is_anom = is_anom.lower() in {"1", "true", "anomaly", "abnormal", "defect"}
        scores.append(float(score))
        labels.append(1 if bool(is_anom) else 0)
    return data, np.asarray(scores, dtype=float), np.asarray(labels, dtype=int)


def load_score_array(data: dict, field_name: str, fallback_field: str | None = None) -> np.ndarray | None:
    values = []
    for sample in data.get("samples", []):
        if field_name in sample:
            values.append(float(sample[field_name]))
        elif fallback_field is not None and fallback_field in sample:
            values.append(float(sample[fallback_field]))
        else:
            return None
    return np.asarray(values, dtype=float)


def fpr_at_95_tpr(labels: np.ndarray, scores: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(labels, scores)
    idx = np.where(tpr >= 0.95)[0]
    if len(idx) == 0:
        return float("nan")
    return float(fpr[idx[0]])


def fpr_at_threshold(labels: np.ndarray, scores: np.ndarray, threshold: float) -> float:
    normal = scores[labels == 0]
    if len(normal) == 0:
        return float("nan")
    return float((normal > threshold).mean())


def f1_max(labels: np.ndarray, scores: np.ndarray) -> float:
    precision, recall, _ = precision_recall_curve(labels, scores)
    f1 = 2 * precision * recall / (precision + recall + 1e-12)
    return float(np.nanmax(f1))


def compute_metrics(labels: np.ndarray, scores: np.ndarray) -> dict:
    normal = scores[labels == 0]
    abnormal = scores[labels == 1]
    auc = roc_auc_score(labels, scores) if len(set(labels.tolist())) == 2 else float("nan")
    normal_p95 = np.percentile(normal, 95)
    abnormal_median = np.median(abnormal)
    false_alarm_proxy = float((normal >= abnormal_median).mean())
    return {
        "auc": float(auc),
        "fpr95tpr": fpr_at_95_tpr(labels, scores),
        "f1max": f1_max(labels, scores),
        "normal_mean": float(normal.mean()),
        "normal_p95": float(normal_p95),
        "abnormal_mean": float(abnormal.mean()),
        "gap": float(abnormal.mean() - normal.mean()),
        "false_alarm_proxy": false_alarm_proxy,
    }


def summarize_one(path: Path) -> dict:
    data, scores, labels = load_scores(path)
    raw_scores = load_score_array(data, "raw_image_score")
    calibrated_scores = load_score_array(data, "calibrated_image_score", fallback_field="image_score")

    if raw_scores is not None and calibrated_scores is not None:
        raw = compute_metrics(labels, raw_scores)
        calibrated = compute_metrics(labels, calibrated_scores)
        thresholds = data.get("thresholds", {})
        raw_threshold = float(thresholds.get("raw_clean_q95", np.nan))
        cal_threshold = float(thresholds.get("calibrated", 1.0))
        return {
            "category": data.get("category", ""),
            "degradation": data.get("degradation", ""),
            "memory_mode": data.get("memory_mode", ""),
            **{f"raw_{key}": value for key, value in raw.items()},
            **{f"cal_{key}": value for key, value in calibrated.items()},
            "raw_fixed_threshold_fpr": fpr_at_threshold(labels, raw_scores, raw_threshold),
            "cal_fixed_threshold_fpr": fpr_at_threshold(labels, calibrated_scores, cal_threshold),
            "raw_threshold": raw_threshold,
            "cal_threshold": cal_threshold,
            "path": str(path),
        }

    metrics = compute_metrics(labels, scores)
    return {
        "category": data.get("category", ""),
        "degradation": data.get("degradation", ""),
        "memory_mode": data.get("memory_mode", ""),
        **metrics,
        "path": str(path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate DRA result JSON files with additional metrics.")
    parser.add_argument("--result_dir", required=True, help="Directory containing result json files.")
    parser.add_argument("--output_csv", required=True, help="Output CSV path.")
    parser.add_argument("--output_md", required=True, help="Output Markdown path.")
    args = parser.parse_args()

    paths = sorted(Path(args.result_dir).glob("*.json"))
    rows = [summarize_one(path) for path in paths]
    df = pd.DataFrame(rows)
    output_csv = Path(args.output_csv)
    output_md = Path(args.output_md)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    lines = ["# DRA Metrics Report\n"]
    if len(df):
        show = df.sort_values(["category", "degradation", "memory_mode"])
        has_calibration = "cal_auc" in show.columns
        if has_calibration:
            lines.append(
                "| Category | Degradation | Mode | Raw AUC | Cal AUC | Raw FPR@95TPR | Cal FPR@95TPR | Raw F1-max | Cal F1-max | Raw Normal P95 | Cal Normal P95 | Raw Fixed FPR | Cal Fixed FPR | Raw Gap | Cal Gap |"
            )
            lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
            for _, row in show.iterrows():
                lines.append(
                    f"| {row['category']} | {row['degradation']} | {row['memory_mode']} | "
                    f"{row['raw_auc']:.4f} | {row['cal_auc']:.4f} | "
                    f"{row['raw_fpr95tpr']:.4f} | {row['cal_fpr95tpr']:.4f} | "
                    f"{row['raw_f1max']:.4f} | {row['cal_f1max']:.4f} | "
                    f"{row['raw_normal_p95']:.4f} | {row['cal_normal_p95']:.4f} | "
                    f"{row['raw_fixed_threshold_fpr']:.4f} | {row['cal_fixed_threshold_fpr']:.4f} | "
                    f"{row['raw_gap']:.4f} | {row['cal_gap']:.4f} |"
                )
        else:
            lines.append(
                "| Category | Degradation | Mode | AUC | FPR@95TPR | F1-max | Normal Mean | Normal P95 | Gap | False Alarm Proxy |"
            )
            lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|")
            for _, row in show.iterrows():
                lines.append(
                    f"| {row['category']} | {row['degradation']} | {row['memory_mode']} | "
                    f"{row['auc']:.4f} | {row['fpr95tpr']:.4f} | {row['f1max']:.4f} | "
                    f"{row['normal_mean']:.4f} | {row['normal_p95']:.4f} | "
                    f"{row['gap']:.4f} | {row['false_alarm_proxy']:.4f} |"
                )

    output_md.write_text("\n".join(lines), encoding="utf-8")
    print("Saved:", output_csv)
    print("Saved:", output_md)


if __name__ == "__main__":
    main()
