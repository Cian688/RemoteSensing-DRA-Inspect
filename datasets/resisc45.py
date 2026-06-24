from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .remote_sensing import build_one_class_protocol, collect_scene_folders

RESISC45_SELECTED_CLASSES = (
    "airport",
    "bridge",
    "commercial_area",
    "dense_residential",
    "forest",
    "freeway",
    "harbor",
    "industrial_area",
    "meadow",
    "mountain",
    "parking_lot",
    "railway_station",
    "river",
    "runway",
    "storage_tank",
)

RESISC45_HARD_ANOMALIES = {
    "dense_residential": ("commercial_area", "industrial_area", "parking_lot"),
    "forest": ("meadow", "mountain"),
    "river": ("harbor", "bridge"),
    "freeway": ("runway", "railway_station"),
    "industrial_area": ("commercial_area", "storage_tank", "dense_residential"),
}

RESISC45_HARD_PROTOCOLS = {
    "urban_dense": {
        "normal": ("dense_residential",),
        "anomaly": ("commercial_area", "industrial_area"),
    },
    "vegetation_forest": {
        "normal": ("forest",),
        "anomaly": ("meadow", "mountain"),
    },
    "infrastructure_airport": {
        "normal": ("airport",),
        "anomaly": ("runway", "parking_lot", "railway_station"),
    },
}


def collect_resisc45_folders(root: str | Path) -> dict[str, list[Path]]:
    return collect_scene_folders(root)


def build_resisc45_protocol(
    *,
    root: str | Path,
    normal_class: str,
    seed: int,
    protocol: str = "one_vs_rest",
    hard_protocol: str | None = None,
    train_ratio: float = 0.8,
    anomaly_classes: Sequence[str] | None = None,
    max_anomaly_test_samples_per_class: int | None = None,
) -> dict[str, object]:
    protocol_name = protocol
    if protocol == "hard":
        if hard_protocol is not None:
            spec = RESISC45_HARD_PROTOCOLS.get(hard_protocol)
            if spec is None:
                raise KeyError(f"Unknown NWPU-RESISC45 hard protocol: '{hard_protocol}'.")
            normal_candidates = tuple(spec["normal"])
            if normal_class and normal_class not in normal_candidates:
                raise ValueError(
                    f"hard_protocol '{hard_protocol}' requires normal_class='{normal_candidates[0]}', "
                    f"but got '{normal_class}'."
                )
            normal_class = normal_candidates[0]
            anomaly_classes = tuple(spec["anomaly"])
            protocol_name = hard_protocol
        elif anomaly_classes is None:
            anomaly_classes = RESISC45_HARD_ANOMALIES.get(normal_class)
            if anomaly_classes is None:
                raise KeyError(
                    f"No default hard-anomaly set is defined for NWPU-RESISC45 class '{normal_class}'."
                )

    bundle = build_one_class_protocol(
        dataset_name="resisc45",
        scene_to_images=collect_resisc45_folders(root),
        normal_class=normal_class,
        protocol=protocol,
        seed=seed,
        train_ratio=train_ratio,
        scene_classes=RESISC45_SELECTED_CLASSES,
        anomaly_classes=anomaly_classes,
        max_anomaly_test_samples_per_class=max_anomaly_test_samples_per_class,
    )
    bundle["protocol_name"] = protocol_name
    bundle["normal_classes"] = [bundle["normal_class"]]
    return bundle
