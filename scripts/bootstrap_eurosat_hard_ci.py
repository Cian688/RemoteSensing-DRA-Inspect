from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from utils.metrics import binary_auc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Bootstrap confidence intervals for EuroSAT-Hard main results using stored per-sample scores. "
            "This script resamples test samples within each protocol/degradation result file and reports "
            "CIs for the averaged-by-setting metrics."
        )
    )
    parser.add_argument(
        "--input_dir",
        default="outputs/remote_sensing/results/eurosat_hard_main",
        help="Directory containing EuroSAT-Hard result JSON files.",
    )
    parser.add_argument(
        "--output_csv",
        default="outputs/remote_sensing/results/eurosat_hard_main/bootstrap_ci_summary.csv",
        help="Output CSV path.",
    )
    parser.add_argument(
        "--output_md",
        default="outputs/remote_sensing/results/eurosat_hard_main/bootstrap_ci_summary.md",
        help="Output Markdown path.",
    )
    parser.add_argument(
        "--output_delta_csv",
        default="outputs/remote_sensing/results/eurosat_hard_main/bootstrap_ci_delta_summary.csv",
        help="Output CSV path for paired delta bootstrap results.",
    )
    parser.add_argument(
        "--num_bootstrap",
        type=int,
        default=1000,
        help="Number of bootstrap resamples.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for bootstrap resampling.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fmt(value: float) -> str:
    return f"{value:.4f}"


def infer_method_name(memory: str, threshold: str) -> str:
    if memory == "clean" and threshold == "clean_fixed":
        return "PatchCore-CF"
    if memory == "clean" and threshold == "corruption_agnostic":
        return "PatchCore-AC"
    if memory == "mixed" and threshold == "clean_fixed":
        return "DRA-Inspect-CF"
    if memory == "mixed" and threshold == "corruption_agnostic":
        return "DRA-Inspect-AC"
    return f"{memory}-{threshold}"


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
    return {"fpr": fpr, "tpr": tpr, "f1": f1, "bacc": bacc}


def percentile_bounds(values: list[float]) -> tuple[float, float]:
    lower, upper = np.percentile(np.asarray(values, dtype=np.float64), [2.5, 97.5])
    return float(lower), float(upper)


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def load_method_payloads(input_dir: Path) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for json_path in sorted(input_dir.glob("*.json")):
        payload = load_json(json_path)
        samples = payload["samples"]
        labels = np.asarray([1 if bool(sample["is_anomalous"]) else 0 for sample in samples], dtype=np.int32)
        raw_scores = np.asarray([float(sample["raw_image_score"]) for sample in samples], dtype=np.float32)
        calibrated_scores = np.asarray(
            [float(sample["corruption_agnostic_image_score"]) for sample in samples], dtype=np.float32
        )

        grouped["PatchCore-CF" if payload["base_memory_mode"] == "clean" else "DRA-Inspect-CF"].append(
            {
                "protocol": str(payload.get("protocol_key", payload.get("protocol_name"))),
                "degradation": str(payload["degradation"]),
                "labels": labels,
                "scores": raw_scores,
                "threshold": float(payload["protocol_metrics"]["clean_fixed"]["threshold"]),
            }
        )
        grouped["PatchCore-AC" if payload["base_memory_mode"] == "clean" else "DRA-Inspect-AC"].append(
            {
                "protocol": str(payload.get("protocol_key", payload.get("protocol_name"))),
                "degradation": str(payload["degradation"]),
                "labels": labels,
                "scores": calibrated_scores,
                "threshold": float(payload["protocol_metrics"]["corruption_agnostic"]["threshold"]),
            }
        )
    if not grouped:
        raise SystemExit(f"No JSON files found under: {input_dir}")
    return grouped


def summarize_point_estimates(method_payloads: dict[str, list[dict]]) -> list[dict]:
    rows: list[dict] = []
    for method, payloads in sorted(method_payloads.items()):
        metrics_accum = {"auc": [], "fpr": [], "tpr": [], "f1": [], "bacc": []}
        for payload in payloads:
            labels = payload["labels"]
            scores = payload["scores"]
            threshold = payload["threshold"]
            metrics_accum["auc"].append(float(binary_auc(labels.tolist(), scores.tolist())))
            fixed = fixed_operating_metrics(labels, scores, threshold)
            for key in ("fpr", "tpr", "f1", "bacc"):
                metrics_accum[key].append(float(fixed[key]))
        rows.append(
            {
                "method": method,
                "auc": float(np.mean(metrics_accum["auc"])),
                "fpr": float(np.mean(metrics_accum["fpr"])),
                "tpr": float(np.mean(metrics_accum["tpr"])),
                "f1": float(np.mean(metrics_accum["f1"])),
                "bacc": float(np.mean(metrics_accum["bacc"])),
            }
        )
    return rows


def bootstrap_rows(method_payloads: dict[str, list[dict]], num_bootstrap: int, seed: int) -> list[dict]:
    rng = np.random.default_rng(seed)
    order = ["PatchCore-CF", "PatchCore-AC", "DRA-Inspect-CF", "DRA-Inspect-AC"]
    point_rows = {row["method"]: row for row in summarize_point_estimates(method_payloads)}
    bootstrap_metrics: dict[str, dict[str, list[float]]] = {
        method: {"auc": [], "fpr": [], "tpr": [], "f1": [], "bacc": []}
        for method in method_payloads
    }

    for _ in range(num_bootstrap):
        for method, payloads in method_payloads.items():
            aucs: list[float] = []
            fprs: list[float] = []
            tprs: list[float] = []
            f1s: list[float] = []
            baccs: list[float] = []
            for payload in payloads:
                labels = payload["labels"]
                scores = payload["scores"]
                threshold = payload["threshold"]
                indices = rng.integers(0, len(labels), size=len(labels))
                sampled_labels = labels[indices]
                sampled_scores = scores[indices]
                aucs.append(float(binary_auc(sampled_labels.tolist(), sampled_scores.tolist())))
                fixed = fixed_operating_metrics(sampled_labels, sampled_scores, threshold)
                fprs.append(float(fixed["fpr"]))
                tprs.append(float(fixed["tpr"]))
                f1s.append(float(fixed["f1"]))
                baccs.append(float(fixed["bacc"]))
            bootstrap_metrics[method]["auc"].append(float(np.mean(aucs)))
            bootstrap_metrics[method]["fpr"].append(float(np.mean(fprs)))
            bootstrap_metrics[method]["tpr"].append(float(np.mean(tprs)))
            bootstrap_metrics[method]["f1"].append(float(np.mean(f1s)))
            bootstrap_metrics[method]["bacc"].append(float(np.mean(baccs)))

    rows: list[dict] = []
    for method in order:
        point = point_rows[method]
        row = {"method": method}
        for metric in ("auc", "fpr", "tpr", "f1", "bacc"):
            low, high = percentile_bounds(bootstrap_metrics[method][metric])
            row[metric] = point[metric]
            row[f"{metric}_low"] = low
            row[f"{metric}_high"] = high
        rows.append(row)
    return rows


def bootstrap_delta_rows(method_payloads: dict[str, list[dict]], num_bootstrap: int, seed: int) -> list[dict]:
    rng = np.random.default_rng(seed)
    pair_specs = [
        ("DRA-CF - PatchCore-CF", "DRA-Inspect-CF", "PatchCore-CF"),
        ("DRA-AC - PatchCore-AC", "DRA-Inspect-AC", "PatchCore-AC"),
    ]
    point_rows = {row["method"]: row for row in summarize_point_estimates(method_payloads)}
    indexed: dict[str, dict[tuple[str, str], dict]] = {}
    for method, payloads in method_payloads.items():
        indexed[method] = {
            (str(payload["protocol"]), str(payload["degradation"])): payload
            for payload in payloads
        }

    output_rows: list[dict] = []
    for label, lhs_method, rhs_method in pair_specs:
        lhs_index = indexed[lhs_method]
        rhs_index = indexed[rhs_method]
        shared_keys = sorted(set(lhs_index.keys()) & set(rhs_index.keys()))
        if not shared_keys:
            continue

        point_delta = {
            "comparison": label,
            "delta_auc": float(point_rows[lhs_method]["auc"] - point_rows[rhs_method]["auc"]),
            "delta_fpr": float(point_rows[lhs_method]["fpr"] - point_rows[rhs_method]["fpr"]),
            "delta_tpr": float(point_rows[lhs_method]["tpr"] - point_rows[rhs_method]["tpr"]),
            "delta_f1": float(point_rows[lhs_method]["f1"] - point_rows[rhs_method]["f1"]),
            "delta_bacc": float(point_rows[lhs_method]["bacc"] - point_rows[rhs_method]["bacc"]),
        }
        sampled_metrics = {key: [] for key in ("delta_auc", "delta_fpr", "delta_tpr", "delta_f1", "delta_bacc")}

        for _ in range(num_bootstrap):
            delta_aucs: list[float] = []
            delta_fprs: list[float] = []
            delta_tprs: list[float] = []
            delta_f1s: list[float] = []
            delta_baccs: list[float] = []
            for key in shared_keys:
                lhs_payload = lhs_index[key]
                rhs_payload = rhs_index[key]
                lhs_labels = lhs_payload["labels"]
                rhs_labels = rhs_payload["labels"]
                if lhs_labels.shape != rhs_labels.shape or not np.array_equal(lhs_labels, rhs_labels):
                    raise ValueError(f"Mismatched labels for paired bootstrap at {label} / {key}")
                indices = rng.integers(0, len(lhs_labels), size=len(lhs_labels))
                sampled_labels = lhs_labels[indices]
                lhs_scores = lhs_payload["scores"][indices]
                rhs_scores = rhs_payload["scores"][indices]
                lhs_fixed = fixed_operating_metrics(sampled_labels, lhs_scores, lhs_payload["threshold"])
                rhs_fixed = fixed_operating_metrics(sampled_labels, rhs_scores, rhs_payload["threshold"])
                delta_aucs.append(
                    float(binary_auc(sampled_labels.tolist(), lhs_scores.tolist()))
                    - float(binary_auc(sampled_labels.tolist(), rhs_scores.tolist()))
                )
                delta_fprs.append(float(lhs_fixed["fpr"] - rhs_fixed["fpr"]))
                delta_tprs.append(float(lhs_fixed["tpr"] - rhs_fixed["tpr"]))
                delta_f1s.append(float(lhs_fixed["f1"] - rhs_fixed["f1"]))
                delta_baccs.append(float(lhs_fixed["bacc"] - rhs_fixed["bacc"]))
            sampled_metrics["delta_auc"].append(float(np.mean(delta_aucs)))
            sampled_metrics["delta_fpr"].append(float(np.mean(delta_fprs)))
            sampled_metrics["delta_tpr"].append(float(np.mean(delta_tprs)))
            sampled_metrics["delta_f1"].append(float(np.mean(delta_f1s)))
            sampled_metrics["delta_bacc"].append(float(np.mean(delta_baccs)))

        for metric in ("delta_auc", "delta_fpr", "delta_tpr", "delta_f1", "delta_bacc"):
            low, high = percentile_bounds(sampled_metrics[metric])
            point_delta[f"{metric}_low"] = low
            point_delta[f"{metric}_high"] = high
        output_rows.append(point_delta)
    return output_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "method",
        "auc",
        "auc_low",
        "auc_high",
        "fpr",
        "fpr_low",
        "fpr_high",
        "tpr",
        "tpr_low",
        "tpr_high",
        "f1",
        "f1_low",
        "f1_high",
        "bacc",
        "bacc_low",
        "bacc_high",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_delta_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "comparison",
        "delta_auc",
        "delta_auc_low",
        "delta_auc_high",
        "delta_fpr",
        "delta_fpr_low",
        "delta_fpr_high",
        "delta_tpr",
        "delta_tpr_low",
        "delta_tpr_high",
        "delta_f1",
        "delta_f1_low",
        "delta_f1_high",
        "delta_bacc",
        "delta_bacc_low",
        "delta_bacc_high",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict], delta_rows: list[dict], num_bootstrap: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [f"# EuroSAT-Hard Bootstrap CI Summary ({num_bootstrap} resamples)", ""]
    lines.append("## Point Estimates With Confidence Intervals")
    lines.append("")
    lines.extend(
        markdown_table(
            ["Method", "AUROC", "FPR", "TPR", "F1", "BAcc"],
            [
                [
                    str(row["method"]),
                    f"{fmt(float(row['auc']))} [{fmt(float(row['auc_low']))}, {fmt(float(row['auc_high']))}]",
                    f"{fmt(float(row['fpr']))} [{fmt(float(row['fpr_low']))}, {fmt(float(row['fpr_high']))}]",
                    f"{fmt(float(row['tpr']))} [{fmt(float(row['tpr_low']))}, {fmt(float(row['tpr_high']))}]",
                    f"{fmt(float(row['f1']))} [{fmt(float(row['f1_low']))}, {fmt(float(row['f1_high']))}]",
                    f"{fmt(float(row['bacc']))} [{fmt(float(row['bacc_low']))}, {fmt(float(row['bacc_high']))}]",
                ]
                for row in rows
            ],
        )
    )
    lines.append("")
    if delta_rows:
        lines.append("## Paired Delta Confidence Intervals")
        lines.append("")
        lines.extend(
            markdown_table(
                ["Comparison", "Delta AUROC", "Delta FPR", "Delta TPR", "Delta F1", "Delta BAcc"],
                [
                    [
                        str(row["comparison"]),
                        f"{fmt(float(row['delta_auc']))} [{fmt(float(row['delta_auc_low']))}, {fmt(float(row['delta_auc_high']))}]",
                        f"{fmt(float(row['delta_fpr']))} [{fmt(float(row['delta_fpr_low']))}, {fmt(float(row['delta_fpr_high']))}]",
                        f"{fmt(float(row['delta_tpr']))} [{fmt(float(row['delta_tpr_low']))}, {fmt(float(row['delta_tpr_high']))}]",
                        f"{fmt(float(row['delta_f1']))} [{fmt(float(row['delta_f1_low']))}, {fmt(float(row['delta_f1_high']))}]",
                        f"{fmt(float(row['delta_bacc']))} [{fmt(float(row['delta_bacc_low']))}, {fmt(float(row['delta_bacc_high']))}]",
                    ]
                    for row in delta_rows
                ],
            )
        )
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = REPO_ROOT / args.input_dir
    method_payloads = load_method_payloads(input_dir)
    rows = bootstrap_rows(method_payloads, num_bootstrap=int(args.num_bootstrap), seed=int(args.seed))
    delta_rows = bootstrap_delta_rows(method_payloads, num_bootstrap=int(args.num_bootstrap), seed=int(args.seed))
    write_csv(REPO_ROOT / args.output_csv, rows)
    write_delta_csv(REPO_ROOT / args.output_delta_csv, delta_rows)
    write_markdown(REPO_ROOT / args.output_md, rows, delta_rows, int(args.num_bootstrap))

    print("method\tauc\tauc_low\tauc_high\tfpr\tfpr_low\tfpr_high\tf1\tf1_low\tf1_high")
    for row in rows:
        print(
            "\t".join(
                [
                    str(row["method"]),
                    fmt(float(row["auc"])),
                    fmt(float(row["auc_low"])),
                    fmt(float(row["auc_high"])),
                    fmt(float(row["fpr"])),
                    fmt(float(row["fpr_low"])),
                    fmt(float(row["fpr_high"])),
                    fmt(float(row["f1"])),
                    fmt(float(row["f1_low"])),
                    fmt(float(row["f1_high"])),
                ]
            )
        )
    print(f"\nSaved CSV: {args.output_csv}")
    print(f"Saved Delta CSV: {args.output_delta_csv}")
    print(f"Saved Markdown: {args.output_md}")


if __name__ == "__main__":
    main()
