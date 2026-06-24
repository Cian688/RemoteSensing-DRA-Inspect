from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Iterable, Sequence

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def normalize_scene_label(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


@dataclass(frozen=True)
class RemoteSensingSample:
    dataset_name: str
    scene_label: str
    image_path: Path
    split: str
    is_normal: bool
    normal_class: str
    protocol: str

    @property
    def label(self) -> str:
        return "normal" if self.is_normal else "anomaly"

    @property
    def is_anomalous(self) -> bool:
        return not self.is_normal


def _iter_images(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(path for path in folder.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)


def _collect_scene_folders_from_root(dataset_root: Path) -> dict[str, list[Path]]:
    scene_to_images: dict[str, list[Path]] = {}
    for scene_dir in sorted(path for path in dataset_root.iterdir() if path.is_dir()):
        images = _iter_images(scene_dir)
        if images:
            scene_to_images[scene_dir.name] = images
    return scene_to_images


def collect_scene_folders(root: str | Path) -> dict[str, list[Path]]:
    dataset_root = Path(root)
    if not dataset_root.exists():
        raise FileNotFoundError(f"Remote sensing dataset root not found: {dataset_root}")

    scene_to_images = _collect_scene_folders_from_root(dataset_root)
    if scene_to_images:
        return scene_to_images

    # Some public remote sensing datasets add one container directory such as
    # "2750" before the actual per-class folders. Support that layout directly.
    child_dirs = sorted(path for path in dataset_root.iterdir() if path.is_dir())
    if len(child_dirs) == 1:
        scene_to_images = _collect_scene_folders_from_root(child_dirs[0])
    if not scene_to_images:
        raise ValueError(f"No scene folders with images were found under: {dataset_root}")
    return scene_to_images


def resolve_scene_names(available_names: Iterable[str], requested_names: Sequence[str]) -> list[str]:
    normalized = {normalize_scene_label(name): name for name in available_names}
    resolved: list[str] = []
    missing: list[str] = []
    for requested in requested_names:
        key = normalize_scene_label(requested)
        matched = normalized.get(key)
        if matched is None:
            missing.append(requested)
        elif matched not in resolved:
            resolved.append(matched)
    if missing:
        raise KeyError(f"Could not resolve scene classes: {missing}")
    return resolved


def _rng_choice(items: list[Path], count: int, seed: int) -> list[Path]:
    if count >= len(items):
        return list(items)
    import numpy as np

    rng = np.random.default_rng(seed)
    indices = np.sort(rng.choice(len(items), size=count, replace=False))
    return [items[idx] for idx in indices]


def build_one_class_protocol(
    *,
    dataset_name: str,
    scene_to_images: dict[str, list[Path]],
    normal_class: str,
    protocol: str,
    seed: int,
    train_ratio: float = 0.8,
    scene_classes: Sequence[str] | None = None,
    anomaly_classes: Sequence[str] | None = None,
    max_anomaly_test_samples_per_class: int | None = None,
) -> dict[str, object]:
    import numpy as np

    available_names = list(scene_to_images.keys())
    if scene_classes is not None:
        resolved_scene_classes = resolve_scene_names(available_names, list(scene_classes))
        scene_to_images = {name: scene_to_images[name] for name in resolved_scene_classes}
        available_names = list(scene_to_images.keys())
    else:
        resolved_scene_classes = available_names

    resolved_normal = resolve_scene_names(available_names, [normal_class])[0]
    if anomaly_classes is None:
        resolved_anomalies = [name for name in available_names if name != resolved_normal]
    else:
        resolved_anomalies = resolve_scene_names(
            [name for name in available_names if name != resolved_normal],
            list(anomaly_classes),
        )

    normal_images = list(scene_to_images[resolved_normal])
    if len(normal_images) < 2:
        raise ValueError(f"Need at least two normal images for class '{resolved_normal}'.")

    rng = np.random.default_rng(seed)
    order = rng.permutation(len(normal_images))
    train_count = int(round(len(normal_images) * train_ratio))
    train_count = min(max(1, train_count), len(normal_images) - 1)
    train_indices = set(order[:train_count].tolist())

    train_samples: list[RemoteSensingSample] = []
    test_samples: list[RemoteSensingSample] = []

    for idx, image_path in enumerate(normal_images):
        split = "train" if idx in train_indices else "test"
        sample = RemoteSensingSample(
            dataset_name=dataset_name,
            scene_label=resolved_normal,
            image_path=image_path,
            split=split,
            is_normal=True,
            normal_class=resolved_normal,
            protocol=protocol,
        )
        if split == "train":
            train_samples.append(sample)
        else:
            test_samples.append(sample)

    anomaly_cap_per_class = max_anomaly_test_samples_per_class
    if resolved_anomalies and anomaly_cap_per_class is None:
        # Keep the binary test prior roughly balanced by default so that fixed
        # F1 remains comparable across normal classes and datasets.
        normal_test_count = len(test_samples)
        anomaly_cap_per_class = max(1, int(ceil(normal_test_count / len(resolved_anomalies))))

    for anomaly_offset, scene_name in enumerate(resolved_anomalies):
        scene_images = list(scene_to_images[scene_name])
        if anomaly_cap_per_class is not None:
            scene_images = _rng_choice(
                scene_images,
                count=anomaly_cap_per_class,
                seed=seed + anomaly_offset + 1,
            )
        for image_path in scene_images:
            test_samples.append(
                RemoteSensingSample(
                    dataset_name=dataset_name,
                    scene_label=scene_name,
                    image_path=image_path,
                    split="test",
                    is_normal=False,
                    normal_class=resolved_normal,
                    protocol=protocol,
                )
            )

    return {
        "dataset_name": dataset_name,
        "scene_classes": resolved_scene_classes,
        "normal_class": resolved_normal,
        "anomaly_classes": resolved_anomalies,
        "anomaly_cap_per_class": anomaly_cap_per_class,
        "train_samples": train_samples,
        "test_samples": test_samples,
    }
