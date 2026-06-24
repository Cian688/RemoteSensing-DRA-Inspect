from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
from torchvision.models import Wide_ResNet50_2_Weights, wide_resnet50_2


@dataclass
class PatchCoreBackboneOutput:
    features: np.ndarray
    grid_shape: Tuple[int, int]


class WideResNetPatchCoreBackbone:
    def __init__(
        self,
        image_size: int = 224,
        pretrained: bool = True,
        layers: Iterable[str] = ("layer2", "layer3"),
        device: str = "cpu",
    ) -> None:
        self.image_size = image_size
        self.layers = tuple(layers)
        self.device = torch.device(device)
        weights = Wide_ResNet50_2_Weights.IMAGENET1K_V1 if pretrained else None
        self.model = wide_resnet50_2(weights=weights)
        self.model.eval().to(self.device)
        self._activations: Dict[str, torch.Tensor] = {}
        self._hooks = []
        self._register_hooks()
        self.transform = transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=(0.485, 0.456, 0.406),
                    std=(0.229, 0.224, 0.225),
                ),
            ]
        )

    def _register_hooks(self) -> None:
        modules = dict(self.model.named_modules())
        for layer_name in self.layers:
            if layer_name not in modules:
                raise ValueError(f"Unsupported backbone layer: {layer_name}")
            module = modules[layer_name]
            self._hooks.append(module.register_forward_hook(self._capture(layer_name)))

    def _capture(self, layer_name: str):
        def hook(_module, _inputs, output) -> None:
            self._activations[layer_name] = output.detach()

        return hook

    def _merge_feature_maps(self) -> torch.Tensor:
        feature_maps = [self._activations[name] for name in self.layers]
        target_h, target_w = feature_maps[-1].shape[-2:]
        resized = []
        for feature_map in feature_maps:
            if feature_map.shape[-2:] != (target_h, target_w):
                feature_map = F.adaptive_avg_pool2d(feature_map, (target_h, target_w))
            resized.append(feature_map)
        return torch.cat(resized, dim=1)

    @torch.inference_mode()
    def extract(self, image: Image.Image) -> PatchCoreBackboneOutput:
        tensor = self.transform(image.convert("RGB")).unsqueeze(0).to(self.device)
        self._activations.clear()
        _ = self.model(tensor)
        embedding = self._merge_feature_maps()
        _, channels, height, width = embedding.shape
        patches = embedding.permute(0, 2, 3, 1).reshape(height * width, channels)
        return PatchCoreBackboneOutput(
            features=patches.cpu().numpy().astype(np.float32),
            grid_shape=(height, width),
        )
