from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

from calibration import ReliabilityCalibrator
from datasets import collect_mvtec_samples
from memory import DegradationMemoryBank
from models import SimplePatchBackbone
from selector import RuleBasedQualitySelector
from utils.config import load_config
from utils.io import ensure_dir, write_json
from utils.metrics import binary_auc, summarize_scores


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Evaluate DRA-Inspect on MVTec AD.')
    parser.add_argument('--config', type=str, required=True, help='Path to YAML config file.')
    parser.add_argument('--category', type=str, default=None, help='Single MVTec category override.')
    return parser.parse_args()


def image_score_from_patches(scores: np.ndarray, topk_ratio: float) -> float:
    k = max(1, int(round(len(scores) * topk_ratio)))
    return float(np.mean(np.sort(scores)[-k:]))


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    dataset_root = config['dataset']['root']
    categories = [args.category] if args.category else list(config['dataset']['categories'])
    output_root = Path(config['output']['root'])
    bank_root = output_root / 'banks'
    results_root = ensure_dir(output_root / 'results')
    topk_ratio = float(config['scoring'].get('topk_ratio', 0.1))
    degradation_names = list(config['degradations']['train'])
    backbone = SimplePatchBackbone(
        image_size=int(config['feature_extractor']['image_size']),
        patch_size=int(config['feature_extractor']['patch_size']),
    )
    selector = RuleBasedQualitySelector(
        degradations=degradation_names,
        min_weight=float(config['selector'].get('min_weight', 0.05)),
    )
    calibrator = ReliabilityCalibrator(
        disagreement_scale=float(config['calibration'].get('disagreement_scale', 0.35)),
    )

    for category in categories:
        bank_path = bank_root / f'{category}_memory.npz'
        if not bank_path.exists():
            raise FileNotFoundError(f'Memory bank not found for {category}: {bank_path}')
        bank = DegradationMemoryBank.load(bank_path)
        samples = collect_mvtec_samples(dataset_root, category=category, split='test')
        labels = []
        raw_scores = []
        calibrated_scores = []
        per_sample = []

        for sample in tqdm(samples, desc=f'Evaluating {category}'):
            image = Image.open(sample.image_path).convert('RGB')
            weights = selector.compute_weights(image)
            output = backbone.extract(image)
            raw_patch_scores, per_bank_scores = bank.weighted_patch_scores(output.features, weights)
            calibrated_patch_scores, reliability = calibrator.calibrate(raw_patch_scores, per_bank_scores)
            raw_score = image_score_from_patches(raw_patch_scores, topk_ratio=topk_ratio)
            calibrated_score = image_score_from_patches(calibrated_patch_scores, topk_ratio=topk_ratio)
            labels.append(1 if sample.is_anomalous else 0)
            raw_scores.append(raw_score)
            calibrated_scores.append(calibrated_score)
            per_sample.append(
                {
                    'image_path': str(sample.image_path),
                    'label': sample.label,
                    'is_anomalous': sample.is_anomalous,
                    'raw_score': raw_score,
                    'calibrated_score': calibrated_score,
                    'reliability': reliability,
                    'weights': weights,
                }
            )

        summary = {
            'category': category,
            'num_samples': len(samples),
            'raw_image_auc': binary_auc(labels, raw_scores),
            'calibrated_image_auc': binary_auc(labels, calibrated_scores),
            'raw_score_stats': summarize_scores(raw_scores),
            'calibrated_score_stats': summarize_scores(calibrated_scores),
            'samples': per_sample,
        }
        write_json(results_root / f'{category}_results.json', summary)
        print(f'[{category}] raw AUC={summary["raw_image_auc"]:.4f}, calibrated AUC={summary["calibrated_image_auc"]:.4f}')


if __name__ == '__main__':
    main()
