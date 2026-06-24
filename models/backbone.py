from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
from PIL import Image


@dataclass
class BackboneOutput:
    features: np.ndarray
    grid_shape: Tuple[int, int]


class SimplePatchBackbone:
    def __init__(self, image_size: int = 256, patch_size: int = 16) -> None:
        if image_size % patch_size != 0:
            raise ValueError('image_size must be divisible by patch_size')
        self.image_size = image_size
        self.patch_size = patch_size

    def extract(self, image: Image.Image) -> BackboneOutput:
        image = image.convert('RGB').resize((self.image_size, self.image_size))
        array = np.asarray(image).astype(np.float32) / 255.0
        h, w, c = array.shape
        p = self.patch_size
        gh, gw = h // p, w // p
        patches = array.reshape(gh, p, gw, p, c).transpose(0, 2, 1, 3, 4).reshape(gh * gw, p * p, c)
        means = patches.mean(axis=1)
        stds = patches.std(axis=1)
        mins = patches.min(axis=1)
        maxs = patches.max(axis=1)
        features = np.concatenate([means, stds, mins, maxs], axis=1)
        return BackboneOutput(features=features, grid_shape=(gh, gw))
