from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass
class ReliabilityCalibrator:
    """A lightweight calibration helper for the public MVTec scripts.

    The original paper focuses on q50/q95 operating-point calibration for the
    remote sensing experiments. The simplified MVTec scripts in this public
    release use a per-patch reliability weight derived from disagreement across
    degradation-specific banks so that the evaluation entry points remain
    runnable without private training utilities.
    """

    disagreement_scale: float = 0.35

    def calibrate(
        self,
        raw_patch_scores: np.ndarray,
        per_bank_scores: Dict[str, np.ndarray],
    ) -> Tuple[np.ndarray, float]:
        raw_patch_scores = np.asarray(raw_patch_scores, dtype=np.float32)
        if raw_patch_scores.size == 0 or not per_bank_scores:
            return raw_patch_scores, 1.0

        bank_stack = np.stack(
            [np.asarray(scores, dtype=np.float32) for scores in per_bank_scores.values()],
            axis=0,
        )
        disagreement = bank_stack.std(axis=0)
        mean_disagreement = float(np.mean(disagreement))
        reliability = 1.0 / (1.0 + max(0.0, self.disagreement_scale) * mean_disagreement)
        calibrated = raw_patch_scores * reliability
        return calibrated.astype(np.float32), float(reliability)
