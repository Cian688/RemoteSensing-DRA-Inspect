from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .remote_sensing import build_one_class_protocol, collect_scene_folders

EUROSAT_CLASSES = (
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake",
)

EUROSAT_HARD_ANOMALIES = {
    "Residential": ("Industrial", "Highway", "River"),
    "Forest": ("HerbaceousVegetation", "Pasture", "AnnualCrop"),
    "SeaLake": ("River",),
    "Highway": ("Industrial", "Residential", "River"),
    "Industrial": ("Residential", "Highway", "PermanentCrop"),
}

EUROSAT_HARD_PROTOCOLS = {
    "urban_residential": {
        "normal": ("Residential",),
        "anomaly": ("Industrial", "Highway"),
    },
    "vegetation_forest": {
        "normal": ("Forest",),
        "anomaly": ("HerbaceousVegetation", "Pasture", "AnnualCrop"),
    },
    "agriculture_annualcrop": {
        "normal": ("AnnualCrop",),
        "anomaly": ("PermanentCrop", "Pasture", "HerbaceousVegetation"),
    },
    "water_sealake": {
        "normal": ("SeaLake",),
        "anomaly": ("River",),
    },
}


def collect_eurosat_folders(root: str | Path) -> dict[str, list[Path]]:
    return collect_scene_folders(root)


def build_eurosat_protocol(
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
            spec = EUROSAT_HARD_PROTOCOLS.get(hard_protocol)
            if spec is None:
                raise KeyError(f"Unknown EuroSAT hard protocol: '{hard_protocol}'.")
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
            anomaly_classes = EUROSAT_HARD_ANOMALIES.get(normal_class)
            if anomaly_classes is None:
                raise KeyError(
                    f"No default hard-anomaly set is defined for EuroSAT class '{normal_class}'."
                )

    bundle = build_one_class_protocol(
        dataset_name="eurosat",
        scene_to_images=collect_eurosat_folders(root),
        normal_class=normal_class,
        protocol=protocol,
        seed=seed,
        train_ratio=train_ratio,
        scene_classes=EUROSAT_CLASSES,
        anomaly_classes=anomaly_classes,
        max_anomaly_test_samples_per_class=max_anomaly_test_samples_per_class,
    )
    bundle["protocol_name"] = protocol_name
    bundle["normal_classes"] = [bundle["normal_class"]]
    return bundle
