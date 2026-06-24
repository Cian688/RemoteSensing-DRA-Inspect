from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'}


@dataclass(frozen=True)
class MVTecSample:
    category: str
    split: str
    label: str
    image_path: Path
    mask_path: Optional[Path]

    @property
    def is_anomalous(self) -> bool:
        return self.label != 'good'


def _iter_images(folder: Path) -> Iterable[Path]:
    if not folder.exists():
        return []
    return sorted(path for path in folder.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)


def _mask_path(root: Path, category: str, label: str, image_path: Path) -> Optional[Path]:
    if label == 'good':
        return None
    stem = image_path.stem + '_mask.png'
    candidate = root / category / 'ground_truth' / label / stem
    return candidate if candidate.exists() else None


def collect_mvtec_samples(root: str | Path, category: str, split: str) -> List[MVTecSample]:
    dataset_root = Path(root)
    category_root = dataset_root / category / split
    if not category_root.exists():
        raise FileNotFoundError(f'MVTec split not found: {category_root}')

    samples: List[MVTecSample] = []
    for label_dir in sorted(path for path in category_root.iterdir() if path.is_dir()):
        label = label_dir.name
        for image_path in _iter_images(label_dir):
            samples.append(
                MVTecSample(
                    category=category,
                    split=split,
                    label=label,
                    image_path=image_path,
                    mask_path=_mask_path(dataset_root, category, label, image_path),
                )
            )
    return samples
