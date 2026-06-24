from __future__ import annotations

import json
from pathlib import Path

import numpy as np


class PaDiMStatsModel:
    def __init__(
        self,
        feature_dim_subsample: int = 256,
        regularization: float = 0.01,
        seed: int = 42,
    ) -> None:
        self.feature_dim_subsample = int(feature_dim_subsample)
        self.regularization = float(regularization)
        self.seed = int(seed)
        self._buffers: list[np.ndarray] = []
        self.feature_indices: np.ndarray | None = None
        self.mean: np.ndarray | None = None
        self.inv_cov: np.ndarray | None = None
        self.num_patches: int | None = None

    def add(self, features: np.ndarray) -> None:
        features = np.asarray(features, dtype=np.float32)
        if features.ndim != 2:
            raise ValueError(f"Expected 2D feature array, got shape={features.shape}.")
        if self.num_patches is None:
            self.num_patches = int(features.shape[0])
        elif int(features.shape[0]) != self.num_patches:
            raise ValueError(
                f"Inconsistent patch count for PaDiM statistics: "
                f"expected {self.num_patches}, got {features.shape[0]}."
            )
        self._buffers.append(features)

    def finalize(self) -> None:
        if not self._buffers:
            raise ValueError("PaDiM statistics model is empty.")

        stacked = np.stack(self._buffers, axis=0).astype(np.float32)
        _, num_patches, total_dim = stacked.shape
        keep_dim = min(max(1, self.feature_dim_subsample), total_dim)
        rng = np.random.default_rng(self.seed)
        feature_indices = np.sort(rng.choice(total_dim, size=keep_dim, replace=False)).astype(np.int32)
        reduced = stacked[:, :, feature_indices].astype(np.float64)

        mean = reduced.mean(axis=0)
        inv_cov = np.empty((num_patches, keep_dim, keep_dim), dtype=np.float32)
        eye = np.eye(keep_dim, dtype=np.float64)
        denom = max(1, reduced.shape[0] - 1)

        for patch_idx in range(num_patches):
            centered = reduced[:, patch_idx, :] - mean[patch_idx]
            cov = (centered.T @ centered) / denom
            cov = cov + self.regularization * eye
            inv_cov[patch_idx] = np.linalg.pinv(cov).astype(np.float32)

        self.feature_indices = feature_indices
        self.mean = mean.astype(np.float32)
        self.inv_cov = inv_cov

    def mahalanobis(self, features: np.ndarray) -> np.ndarray:
        if self.feature_indices is None or self.mean is None or self.inv_cov is None:
            raise ValueError("PaDiM statistics model has not been finalized.")

        features = np.asarray(features, dtype=np.float32)
        if features.ndim != 2:
            raise ValueError(f"Expected 2D feature array, got shape={features.shape}.")
        if int(features.shape[0]) != int(self.mean.shape[0]):
            raise ValueError(
                f"Inconsistent patch count for PaDiM scoring: expected {self.mean.shape[0]}, "
                f"got {features.shape[0]}."
            )

        reduced = features[:, self.feature_indices].astype(np.float32)
        delta = reduced - self.mean
        quad = np.einsum("pd,pde,pe->p", delta, self.inv_cov, delta, optimize=True)
        return np.sqrt(np.clip(quad, a_min=0.0, a_max=None)).astype(np.float32)

    def save(self, path: str | Path) -> None:
        if self.feature_indices is None or self.mean is None or self.inv_cov is None:
            raise ValueError("PaDiM statistics model has not been finalized.")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        meta = {
            "feature_dim_subsample": self.feature_dim_subsample,
            "regularization": self.regularization,
            "seed": self.seed,
            "num_patches": int(self.mean.shape[0]),
        }
        np.savez_compressed(
            path,
            feature_indices=self.feature_indices,
            mean=self.mean,
            inv_cov=self.inv_cov,
            meta=json.dumps(meta),
        )

    @classmethod
    def load(cls, path: str | Path) -> "PaDiMStatsModel":
        payload = np.load(Path(path), allow_pickle=False)
        meta = json.loads(str(payload["meta"]))
        instance = cls(
            feature_dim_subsample=int(meta["feature_dim_subsample"]),
            regularization=float(meta["regularization"]),
            seed=int(meta["seed"]),
        )
        instance.feature_indices = payload["feature_indices"].astype(np.int32)
        instance.mean = payload["mean"].astype(np.float32)
        instance.inv_cov = payload["inv_cov"].astype(np.float32)
        instance.num_patches = int(meta["num_patches"])
        return instance
