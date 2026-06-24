from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np


class DegradationMemoryBank:
    def __init__(self) -> None:
        self._buffers: Dict[str, list[np.ndarray]] = {}
        self.banks: Dict[str, np.ndarray] = {}

    def add(self, degradation: str, features: np.ndarray) -> None:
        self._buffers.setdefault(degradation, []).append(features.astype(np.float32))

    def finalize(self) -> None:
        self.banks = {
            name: np.concatenate(parts, axis=0) if parts else np.empty((0, 0), dtype=np.float32)
            for name, parts in self._buffers.items()
        }

    def available_degradations(self) -> Iterable[str]:
        return self.banks.keys()

    def nearest_distances(self, features: np.ndarray, degradation: str) -> np.ndarray:
        bank = self.banks.get(degradation)
        if bank is None or bank.size == 0:
            return np.full((features.shape[0],), fill_value=np.inf, dtype=np.float32)
        diff = features[:, None, :] - bank[None, :, :]
        dist = np.linalg.norm(diff, axis=-1)
        return dist.min(axis=1)

    def weighted_patch_scores(self, features: np.ndarray, weights: Dict[str, float]) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        per_bank: Dict[str, np.ndarray] = {}
        total = np.zeros((features.shape[0],), dtype=np.float32)
        for name, weight in weights.items():
            distances = self.nearest_distances(features, name)
            per_bank[name] = distances
            total += float(weight) * distances
        return total, per_bank

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        arrays = {f'bank__{name}': bank for name, bank in self.banks.items()}
        meta = {'degradations': sorted(self.banks.keys())}
        np.savez_compressed(path, **arrays, meta=json.dumps(meta))

    @classmethod
    def load(cls, path: str | Path) -> 'DegradationMemoryBank':
        payload = np.load(Path(path), allow_pickle=False)
        instance = cls()
        for key in payload.files:
            if key.startswith('bank__'):
                instance.banks[key.split('bank__', 1)[1]] = payload[key]
        return instance
