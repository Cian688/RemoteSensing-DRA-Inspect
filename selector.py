from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

import numpy as np
from PIL import Image


@dataclass
class RuleBasedQualitySelector:
    """Generate simple degradation weights from image statistics.

    This selector is intentionally lightweight for the public release. It keeps
    all configured degradations active while slightly down-weighting transforms
    whose proxy statistics are less compatible with the observed image.
    """

    degradations: Iterable[str]
    min_weight: float = 0.05

    def compute_weights(self, image: Image.Image) -> Dict[str, float]:
        array = np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0
        brightness = float(array.mean())
        contrast = float(array.std())
        weights: Dict[str, float] = {}

        for name in self.degradations:
            if name == "clean":
                score = 1.0
            elif name == "light":
                score = 1.0 - abs(brightness - 0.5)
            elif name == "blur":
                score = contrast
            elif name == "noise":
                score = 1.0 - contrast
            else:
                score = 0.8
            weights[name] = max(float(self.min_weight), float(score))

        total = sum(weights.values())
        if total <= 0.0:
            uniform = 1.0 / max(1, len(weights))
            return {name: uniform for name in weights}
        return {name: value / total for name, value in weights.items()}
