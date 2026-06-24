from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch


class PatchCoreMemoryBank:
    def __init__(
        self,
        coreset_sampling_ratio: float = 0.1,
        nn_chunk_size: int = 2048,
        seed: int = 42,
        device: str = "cpu",
        max_bank_size: int | None = None,
    ) -> None:
        self.coreset_sampling_ratio = float(coreset_sampling_ratio)
        self.nn_chunk_size = int(nn_chunk_size)
        self.seed = int(seed)
        self.device = torch.device(device)
        self.max_bank_size = None if max_bank_size is None else int(max_bank_size)
        self._buffers: list[np.ndarray] = []
        self.bank: np.ndarray | None = None
        self._coarse_centroids: np.ndarray | None = None
        self._inverted_lists: list[np.ndarray] | None = None
        self._approx_cache_key: tuple[int, int, int] | None = None

    def add(self, features: np.ndarray) -> None:
        self._buffers.append(features.astype(np.float32))

    def finalize(self) -> None:
        if not self._buffers:
            raise ValueError("PatchCore memory bank is empty.")
        bank = np.concatenate(self._buffers, axis=0).astype(np.float32)
        total = bank.shape[0]
        keep = total
        if 0.0 < self.coreset_sampling_ratio < 1.0:
            keep = max(1, int(round(total * self.coreset_sampling_ratio)))
        if self.max_bank_size is not None:
            keep = min(keep, self.max_bank_size)
        if keep < total:
            rng = np.random.default_rng(self.seed)
            indices = rng.choice(total, size=keep, replace=False)
            bank = bank[np.sort(indices)]
        self.bank = bank
        self._coarse_centroids = None
        self._inverted_lists = None
        self._approx_cache_key = None

    def _nearest_from_bank(self, query: torch.Tensor, bank: torch.Tensor) -> np.ndarray:
        best = torch.full((query.shape[0],), fill_value=torch.inf, device=query.device)
        for start in range(0, bank.shape[0], self.nn_chunk_size):
            chunk = bank[start : start + self.nn_chunk_size]
            distances = torch.cdist(query, chunk)
            best = torch.minimum(best, distances.min(dim=1).values)
        return best.cpu().numpy().astype(np.float32)

    def _train_coarse_centroids(
        self,
        train_bank: np.ndarray,
        num_centroids: int,
        kmeans_iters: int,
    ) -> np.ndarray:
        rng = np.random.default_rng(self.seed)
        init_indices = rng.choice(train_bank.shape[0], size=num_centroids, replace=False)
        centroids = torch.from_numpy(train_bank[init_indices].astype(np.float32)).to(self.device)
        train_tensor = torch.from_numpy(train_bank.astype(np.float32)).to(self.device)

        for _ in range(max(1, kmeans_iters)):
            sums = torch.zeros_like(centroids)
            counts = torch.zeros((num_centroids,), dtype=torch.float32, device=self.device)
            for start in range(0, train_tensor.shape[0], self.nn_chunk_size):
                chunk = train_tensor[start : start + self.nn_chunk_size]
                assignments = torch.cdist(chunk, centroids).argmin(dim=1)
                counts.scatter_add_(0, assignments, torch.ones_like(assignments, dtype=torch.float32))
                sums.index_add_(0, assignments, chunk)

            non_empty = counts > 0
            if torch.any(non_empty):
                centroids[non_empty] = sums[non_empty] / counts[non_empty].unsqueeze(1)
            empty_count = int((~non_empty).sum().item())
            if empty_count > 0:
                refill_indices = rng.choice(train_bank.shape[0], size=empty_count, replace=False)
                centroids[~non_empty] = torch.from_numpy(train_bank[refill_indices].astype(np.float32)).to(self.device)

        return centroids.cpu().numpy().astype(np.float32)

    def build_approx_ivf_index(
        self,
        num_centroids: int = 256,
        train_samples: int = 20000,
        kmeans_iters: int = 6,
    ) -> None:
        if self.bank is None or self.bank.size == 0:
            raise ValueError("PatchCore memory bank has not been finalized.")

        num_centroids = max(1, min(int(num_centroids), int(self.bank.shape[0])))
        train_samples = max(num_centroids, min(int(train_samples), int(self.bank.shape[0])))
        cache_key = (num_centroids, train_samples, int(kmeans_iters))
        if (
            self._coarse_centroids is not None
            and self._inverted_lists is not None
            and self._approx_cache_key == cache_key
        ):
            return

        rng = np.random.default_rng(self.seed)
        if train_samples < self.bank.shape[0]:
            sample_indices = rng.choice(self.bank.shape[0], size=train_samples, replace=False)
            train_bank = self.bank[np.sort(sample_indices)]
        else:
            train_bank = self.bank

        self._coarse_centroids = self._train_coarse_centroids(
            train_bank=train_bank,
            num_centroids=num_centroids,
            kmeans_iters=int(kmeans_iters),
        )

        centroids_tensor = torch.from_numpy(self._coarse_centroids).to(self.device)
        bank_tensor = torch.from_numpy(self.bank.astype(np.float32)).to(self.device)
        lists: list[list[int]] = [[] for _ in range(num_centroids)]
        for start in range(0, bank_tensor.shape[0], self.nn_chunk_size):
            chunk = bank_tensor[start : start + self.nn_chunk_size]
            assignments = torch.cdist(chunk, centroids_tensor).argmin(dim=1).cpu().numpy()
            for local_idx, centroid_idx in enumerate(assignments.tolist()):
                lists[int(centroid_idx)].append(start + local_idx)
        self._inverted_lists = [np.asarray(bucket, dtype=np.int64) for bucket in lists]
        self._approx_cache_key = cache_key

    def _nearest_distances_approx_ivf(
        self,
        features: np.ndarray,
        num_centroids: int = 256,
        nprobe: int = 4,
        train_samples: int = 20000,
        kmeans_iters: int = 6,
        max_candidates: int = 8192,
    ) -> np.ndarray:
        self.build_approx_ivf_index(
            num_centroids=num_centroids,
            train_samples=train_samples,
            kmeans_iters=kmeans_iters,
        )
        if self.bank is None or self._coarse_centroids is None or self._inverted_lists is None:
            raise ValueError("Approximate IVF index has not been built.")

        query = torch.from_numpy(features.astype(np.float32)).to(self.device)
        centroid_bank = torch.from_numpy(self._coarse_centroids.astype(np.float32)).to(self.device)
        centroid_distances = torch.cdist(query, centroid_bank)
        k = max(1, min(int(nprobe), int(centroid_bank.shape[0])))
        top_centroid_indices = centroid_distances.topk(k=k, largest=False).indices.cpu().numpy()
        centroid_priority = centroid_distances.min(dim=0).values.cpu().numpy()

        ordered_centroids = sorted(
            np.unique(top_centroid_indices).tolist(),
            key=lambda idx: float(centroid_priority[int(idx)]),
        )

        candidate_parts: list[np.ndarray] = []
        total_candidates = 0
        for centroid_idx in ordered_centroids:
            bucket = self._inverted_lists[int(centroid_idx)]
            if bucket.size == 0:
                continue
            candidate_parts.append(bucket)
            total_candidates += int(bucket.size)
            if total_candidates >= int(max_candidates):
                break

        if not candidate_parts:
            return self._nearest_from_bank(query, torch.from_numpy(self.bank.astype(np.float32)).to(self.device))

        candidate_indices = np.unique(np.concatenate(candidate_parts, axis=0))
        if candidate_indices.size > int(max_candidates):
            candidate_indices = candidate_indices[: int(max_candidates)]
        candidate_bank = torch.from_numpy(self.bank[candidate_indices].astype(np.float32)).to(self.device)
        return self._nearest_from_bank(query, candidate_bank)

    def nearest_distances(
        self,
        features: np.ndarray,
        retrieval_backend: str = "exact",
        **kwargs,
    ) -> np.ndarray:
        if self.bank is None or self.bank.size == 0:
            raise ValueError("PatchCore memory bank has not been finalized.")
        if retrieval_backend == "approx_ivf":
            return self._nearest_distances_approx_ivf(features, **kwargs)
        if retrieval_backend != "exact":
            raise ValueError(f"Unsupported retrieval backend: {retrieval_backend}")
        query = torch.from_numpy(features.astype(np.float32)).to(self.device)
        bank = torch.from_numpy(self.bank.astype(np.float32)).to(self.device)
        return self._nearest_from_bank(query, bank)

    def save(self, path: str | Path) -> None:
        if self.bank is None:
            raise ValueError("PatchCore memory bank has not been finalized.")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        meta = {
            "coreset_sampling_ratio": self.coreset_sampling_ratio,
            "nn_chunk_size": self.nn_chunk_size,
            "seed": self.seed,
            "max_bank_size": self.max_bank_size,
        }
        np.savez_compressed(path, bank=self.bank, meta=json.dumps(meta))

    @classmethod
    def load(
        cls,
        path: str | Path,
        device: str = "cpu",
    ) -> "PatchCoreMemoryBank":
        payload = np.load(Path(path), allow_pickle=False)
        meta = json.loads(str(payload["meta"]))
        instance = cls(
            coreset_sampling_ratio=float(meta["coreset_sampling_ratio"]),
            nn_chunk_size=int(meta["nn_chunk_size"]),
            seed=int(meta["seed"]),
            device=device,
            max_bank_size=meta.get("max_bank_size"),
        )
        instance.bank = payload["bank"].astype(np.float32)
        return instance
