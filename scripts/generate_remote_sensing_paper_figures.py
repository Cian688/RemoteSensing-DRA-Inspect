from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(REPO_ROOT / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd
from PIL import Image

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from degradations import apply_degradation


FIGURE_DIR = REPO_ROOT / "paper_prcv遥感" / "LaTeX2e_Proceedings_Templates" / "figures"
SUMMARY_CSV = REPO_ROOT / "outputs" / "remote_sensing" / "results" / "eurosat_hard_main" / "final_summary.csv"
THRESHOLD_MD = (
    REPO_ROOT / "outputs" / "remote_sensing" / "results" / "eurosat_hard_main" / "threshold_sensitivity_summary.md"
)
RESULT_DIR = REPO_ROOT / "outputs" / "remote_sensing" / "results" / "eurosat_hard_main"
EUROSAT_ROOT = REPO_ROOT.parent / "data" / "eurosat" / "2750"

COLORS = {
    "patchcore_cf": "#4C72B0",
    "patchcore_ac": "#6BAED6",
    "dra_cf": "#DD8452",
    "dra_ac": "#55A868",
    "normal": "#4C72B0",
    "abnormal": "#DD8452",
    "threshold": "#2F2F2F",
}


@dataclass(frozen=True)
class CaseSpec:
    protocol: str
    degradation: str
    title: str


CASE = CaseSpec(
    protocol="vegetation_forest",
    degradation="blur",
    title="Vegetation-Forest + Blur",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def split_scores(payload: dict, score_key: str) -> tuple[np.ndarray, np.ndarray]:
    normal = []
    abnormal = []
    for sample in payload["samples"]:
        score = float(sample[score_key])
        if bool(sample["is_anomalous"]):
            abnormal.append(score)
        else:
            normal.append(score)
    return np.asarray(normal, dtype=float), np.asarray(abnormal, dtype=float)


def add_box(ax, xy, width, height, text, fc="#F7F7F7", ec="#666666", fontsize=10) -> None:
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2.0,
        xy[1] + height / 2.0,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
    )


def add_arrow(ax, start, end) -> None:
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.2,
        color="#555555",
    )
    ax.add_patch(arrow)


def render_figure1() -> None:
    fig, ax = plt.subplots(figsize=(11.2, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.08, 0.93, "Memory Construction", fontsize=13, weight="bold")
    ax.text(0.08, 0.47, "Deployment and Calibration", fontsize=13, weight="bold")

    add_box(ax, (0.05, 0.72), 0.16, 0.12, "Normal remote-sensing\ntiles")
    add_box(ax, (0.28, 0.72), 0.17, 0.12, "Synthetic degradations\nnoise / blur / light /\nlowres / jpeg")
    add_box(ax, (0.52, 0.72), 0.16, 0.12, "Frozen backbone\npatch features")
    add_box(ax, (0.75, 0.76), 0.18, 0.08, "Clean memory")
    add_box(ax, (0.75, 0.64), 0.18, 0.08, "Mixed memory")

    add_arrow(ax, (0.21, 0.78), (0.28, 0.78))
    add_arrow(ax, (0.45, 0.78), (0.52, 0.78))
    add_arrow(ax, (0.68, 0.80), (0.75, 0.80))
    add_arrow(ax, (0.68, 0.72), (0.75, 0.68))

    add_box(ax, (0.05, 0.24), 0.16, 0.12, "Held-out normal\ncalibration split")
    add_box(ax, (0.28, 0.24), 0.17, 0.12, "Quantile statistics\n$q_{50}, q_{95}$")
    add_box(ax, (0.52, 0.24), 0.16, 0.12, "Degraded test tile\n(normal or anomaly)")
    add_box(ax, (0.75, 0.28), 0.18, 0.08, "Clean-reference\nthreshold")
    add_box(ax, (0.75, 0.16), 0.18, 0.08, "Corruption-agnostic\ncalibration")

    add_arrow(ax, (0.21, 0.30), (0.28, 0.30))
    add_arrow(ax, (0.45, 0.30), (0.75, 0.20))
    add_arrow(ax, (0.68, 0.30), (0.75, 0.32))
    add_arrow(ax, (0.68, 0.30), (0.75, 0.20))
    add_arrow(ax, (0.84, 0.64), (0.84, 0.36))

    ax.text(
        0.52,
        0.57,
        "Nearest-neighbor score against clean or mixed memory\n"
        "Two deployment modes:\n"
        "CF = lower fixed FPR, AC = balanced operating point",
        ha="center",
        va="center",
        fontsize=10.5,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#F3F7FB", edgecolor="#AAB7C4"),
    )

    fig.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / "figure1_remote_sensing_framework.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def render_figure2() -> None:
    image_path = EUROSAT_ROOT / "Residential" / "Residential_870.jpg"
    image = Image.open(image_path).convert("RGB")
    variants = [
        ("Clean", image),
        ("Noise", apply_degradation(image, "noise", severity=1.0)),
        ("Blur", apply_degradation(image, "blur", severity=1.0)),
        ("Light", apply_degradation(image, "light", severity=1.0)),
        ("Lowres", apply_degradation(image, "lowres", severity=1.0)),
        ("JPEG", apply_degradation(image, "jpeg", severity=1.0)),
    ]

    fig, axes = plt.subplots(1, 6, figsize=(13.0, 2.6))
    for ax, (title, panel) in zip(axes, variants):
        ax.imshow(panel)
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    fig.suptitle("Representative EuroSAT tile under the five degradation types", fontsize=13, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(FIGURE_DIR / "figure2_eurosat_degradation_examples.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def payload_paths(protocol: str, degradation: str) -> tuple[Path, Path]:
    protocol_to_normal = {
        "vegetation_forest": "forest",
        "urban_residential": "residential",
        "water_sealake": "sealake",
    }
    prefix = f"eurosat_{protocol_to_normal[protocol]}_{protocol}_{degradation}"
    return (
        RESULT_DIR / f"{prefix}_clean_cal.json",
        RESULT_DIR / f"{prefix}_mixed_cal.json",
    )


def choose_representative_normal(clean_payload: dict, mixed_payload: dict) -> dict:
    clean_by_path = {
        sample["image_path"]: sample
        for sample in clean_payload["samples"]
        if not bool(sample["is_anomalous"])
    }
    clean_threshold = 1.0
    raw_threshold = float(mixed_payload["protocol_metrics"]["clean_fixed"]["threshold"])
    candidates = []
    for sample in mixed_payload["samples"]:
        if bool(sample["is_anomalous"]):
            continue
        paired = clean_by_path.get(sample["image_path"])
        if paired is None:
            continue
        patchcore_ac = float(paired["corruption_agnostic_image_score"])
        dra_cf = float(sample["raw_image_score"])
        dra_ac = float(sample["corruption_agnostic_image_score"])
        ranking = (
            1 if patchcore_ac > clean_threshold else 0,
            1 if dra_ac <= 1.0 else 0,
            1 if dra_cf <= raw_threshold else 0,
            patchcore_ac - dra_ac,
            patchcore_ac,
        )
        candidates.append((ranking, sample["image_path"], patchcore_ac, dra_cf, dra_ac))
    candidates.sort(reverse=True)
    _, image_path, patchcore_ac, dra_cf, dra_ac = candidates[0]
    return {
        "image_path": image_path,
        "patchcore_ac": patchcore_ac,
        "dra_cf": dra_cf,
        "dra_ac": dra_ac,
    }


def add_hist_panel(ax, normal_scores, abnormal_scores, threshold, title, stats_lines):
    ax.hist(normal_scores, bins=18, density=True, alpha=0.65, color=COLORS["normal"], label="Normal")
    ax.hist(abnormal_scores, bins=18, density=True, alpha=0.55, color=COLORS["abnormal"], label="Anomaly")
    ax.axvline(threshold, color=COLORS["threshold"], linestyle="--", linewidth=1.6, label="Threshold")
    ax.set_title(f"{title}\n" + ", ".join(stats_lines), fontsize=9.2)
    ax.set_xlabel("Score")
    ax.set_ylabel("Density")


def render_figure3() -> None:
    clean_path, mixed_path = payload_paths(CASE.protocol, CASE.degradation)
    clean_payload = load_json(clean_path)
    mixed_payload = load_json(mixed_path)
    chosen = choose_representative_normal(clean_payload, mixed_payload)

    image = Image.open(chosen["image_path"]).convert("RGB")
    degraded = apply_degradation(image, CASE.degradation, severity=1.0)

    pc_normal, pc_abnormal = split_scores(clean_payload, "corruption_agnostic_image_score")
    cf_normal, cf_abnormal = split_scores(mixed_payload, "raw_image_score")
    ac_normal, ac_abnormal = split_scores(mixed_payload, "corruption_agnostic_image_score")

    fig, axes = plt.subplots(1, 4, figsize=(16.0, 4.6))
    fig.suptitle("EuroSAT-Hard Score-Shift Case Study: Vegetation-Forest under Blur", fontsize=13, y=0.98)

    axes[0].imshow(degraded)
    axes[0].axis("off")
    axes[0].set_title("Representative degraded normal tile", fontsize=10)
    axes[0].text(
        0.03,
        -0.10,
        "\n".join(
            [
                f"PatchCore-AC: {chosen['patchcore_ac']:.3f}",
                f"DRA-CF raw: {chosen['dra_cf']:.3f}",
                f"DRA-AC: {chosen['dra_ac']:.3f}",
                "Thresholds: 1.0 / raw q95 / 1.0",
            ]
        ),
        transform=axes[0].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="0.75", alpha=0.92),
    )

    add_hist_panel(
        axes[1],
        pc_normal,
        pc_abnormal,
        1.0,
        "PatchCore-AC",
        [
            f"AUROC={clean_payload['protocol_metrics']['corruption_agnostic']['image_auc']:.4f}",
            f"FPR={clean_payload['protocol_metrics']['corruption_agnostic']['fixed_threshold_fpr']:.4f}",
            f"F1={clean_payload['protocol_metrics']['corruption_agnostic']['fixed_threshold_f1']:.4f}",
        ],
    )
    add_hist_panel(
        axes[2],
        cf_normal,
        cf_abnormal,
        float(mixed_payload["protocol_metrics"]["clean_fixed"]["threshold"]),
        "DRA-Inspect-CF",
        [
            f"AUROC={mixed_payload['protocol_metrics']['clean_fixed']['image_auc']:.4f}",
            f"FPR={mixed_payload['protocol_metrics']['clean_fixed']['fixed_threshold_fpr']:.4f}",
            f"F1={mixed_payload['protocol_metrics']['clean_fixed']['fixed_threshold_f1']:.4f}",
        ],
    )
    add_hist_panel(
        axes[3],
        ac_normal,
        ac_abnormal,
        1.0,
        "DRA-Inspect-AC",
        [
            f"AUROC={mixed_payload['protocol_metrics']['corruption_agnostic']['image_auc']:.4f}",
            f"FPR={mixed_payload['protocol_metrics']['corruption_agnostic']['fixed_threshold_fpr']:.4f}",
            f"F1={mixed_payload['protocol_metrics']['corruption_agnostic']['fixed_threshold_f1']:.4f}",
        ],
    )
    handles, labels = axes[3].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 0.02), frameon=False)
    fig.tight_layout(rect=[0, 0.08, 1, 0.90])
    fig.subplots_adjust(bottom=0.20, top=0.74, wspace=0.28)
    fig.savefig(FIGURE_DIR / "figure3_eurosat_score_shift.png", dpi=320, bbox_inches="tight")
    plt.close(fig)


def render_figure4() -> None:
    df = pd.read_csv(SUMMARY_CSV)
    protocol_df = (
        df.groupby(["protocol", "method"])[["fpr", "f1"]]
        .mean()
        .reset_index()
    )
    method_order = ["PatchCore-CF", "PatchCore-AC", "DRA-Inspect-CF", "DRA-Inspect-AC"]
    protocol_order = ["vegetation_forest", "urban_residential", "water_sealake"]
    method_color = {
        "PatchCore-CF": COLORS["patchcore_cf"],
        "PatchCore-AC": COLORS["patchcore_ac"],
        "DRA-Inspect-CF": COLORS["dra_cf"],
        "DRA-Inspect-AC": COLORS["dra_ac"],
    }
    method_marker = {
        "PatchCore-CF": "o",
        "PatchCore-AC": "s",
        "DRA-Inspect-CF": "^",
        "DRA-Inspect-AC": "D",
    }

    fig, axes = plt.subplots(1, 3, figsize=(14.8, 4.8), sharex=True, sharey=True)
    legend_handles = []
    for ax, protocol in zip(axes, protocol_order):
        sub = protocol_df[protocol_df["protocol"] == protocol].copy()
        sub["method"] = pd.Categorical(sub["method"], categories=method_order, ordered=True)
        sub = sub.sort_values("method")
        for _, row in sub.iterrows():
            method = str(row["method"])
            scatter = ax.scatter(
                float(row["fpr"]),
                float(row["f1"]),
                s=120,
                color=method_color[method],
                marker=method_marker[method],
                edgecolors="black",
                linewidths=0.6,
                zorder=3,
            )
            if protocol == protocol_order[0]:
                legend_handles.append(scatter)
        ax.set_title(protocol.replace("_", "-"), fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.25)
        ax.set_xlabel("Fixed FPR", fontsize=10.5)
        ax.tick_params(labelsize=9.5)
    axes[0].set_ylabel("Fixed F1")
    axes[0].set_xlim(0.0, 0.09)
    axes[0].set_ylim(0.45, 0.92)
    fig.suptitle("Protocol-wise CF/AC trade-off on EuroSAT-Hard", fontsize=13, y=0.99)
    fig.legend(
        legend_handles,
        [label.replace("DRA-Inspect", "DRA") for label in method_order],
        loc="upper center",
        ncol=4,
        bbox_to_anchor=(0.5, 0.93),
        frameon=False,
        fontsize=9.5,
        handletextpad=0.4,
        columnspacing=1.2,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    fig.savefig(FIGURE_DIR / "figure4_protocol_tradeoff.png", dpi=360, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    render_figure1()
    render_figure2()
    render_figure3()
    render_figure4()
    print(f"Saved figures to: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
