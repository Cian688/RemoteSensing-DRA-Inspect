from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from tqdm import tqdm

from datasets import collect_mvtec_samples
from degradations import apply_degradation
from memory import PatchCoreMemoryBank
from models import WideResNetPatchCoreBackbone
from utils.config import load_config
from utils.io import ensure_dir, write_json
from utils.metrics import binary_auc, summarize_scores


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Evaluate PatchCore under image degradations.')
    parser.add_argument('--config', type=str, required=True, help='Path to YAML config file.')
    parser.add_argument('--category', type=str, default=None, help='Single MVTec category override.')
    parser.add_argument('--degradation', type=str, default=None, help='Single degradation override.')
    parser.add_argument('--severity', type=float, default=None, help='Optional degradation severity override.')
    return parser.parse_args()


def image_score_from_patches(scores: np.ndarray, topk_ratio: float) -> float:
    k = max(1, int(round(len(scores) * topk_ratio)))
    return float(np.mean(np.sort(scores)[-k:]))


def resolve_device(requested_device: str) -> str:
    if requested_device.startswith('cuda'):
        if torch.cuda.is_available():
            return requested_device
        print('Requested CUDA device is unavailable in the current environment. Falling back to CPU.')
        return 'cpu'
    return requested_device


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    dataset_root = config['dataset']['root']
    categories = [args.category] if args.category else list(config['dataset']['categories'])
    degradation_cfg = config.get('degradation_eval', {})
    degradations = [args.degradation] if args.degradation else list(degradation_cfg.get('degradations', ['noise', 'blur', 'light', 'lowres', 'jpeg']))
    severity = float(args.severity if args.severity is not None else degradation_cfg.get('severity', 1.0))
    output_root = Path(config['output']['root'])
    patchcore_cfg = config['patchcore']
    device = resolve_device(str(patchcore_cfg.get('device', 'cpu')))
    print(f'PatchCore degraded eval device: {device}')
    backbone = WideResNetPatchCoreBackbone(
        image_size=int(config['feature_extractor']['image_size']),
        pretrained=bool(config['feature_extractor'].get('pretrained', True)),
        layers=tuple(config['feature_extractor'].get('layers', ['layer2', 'layer3'])),
        device=device,
    )

    for category in categories:
        bank_path = output_root / 'patchcore' / 'banks' / f'{category}_patchcore.npz'
        if not bank_path.exists():
            raise FileNotFoundError(f'PatchCore bank not found for {category}: {bank_path}')
        bank = PatchCoreMemoryBank.load(bank_path, device=device)
        test_samples = collect_mvtec_samples(dataset_root, category=category, split='test')
        category_summary = []

        for degradation in degradations:
            labels = []
            scores = []
            per_sample = []
            anomaly_maps_dir = ensure_dir(output_root / 'patchcore_degraded' / 'anomaly_maps' / degradation / category)

            for sample in tqdm(test_samples, desc=f'PatchCore {category} {degradation}'):
                image = Image.open(sample.image_path).convert('RGB')
                degraded_image = apply_degradation(image, name=degradation, severity=severity)
                output = backbone.extract(degraded_image)
                patch_scores = bank.nearest_distances(output.features)
                image_score = image_score_from_patches(
                    patch_scores, topk_ratio=float(patchcore_cfg.get('topk_ratio', 0.1))
                )
                labels.append(1 if sample.is_anomalous else 0)
                scores.append(image_score)
                map_name = f'{sample.label}__{sample.image_path.stem}.npy'
                np.save(anomaly_maps_dir / map_name, patch_scores.reshape(output.grid_shape).astype(np.float32))
                per_sample.append(
                    {
                        'image_path': str(sample.image_path),
                        'label': sample.label,
                        'is_anomalous': sample.is_anomalous,
                        'degradation': degradation,
                        'severity': severity,
                        'image_score': image_score,
                    }
                )

            summary = {
                'category': category,
                'degradation': degradation,
                'severity': severity,
                'num_test_samples': len(test_samples),
                'image_auc': binary_auc(labels, scores),
                'score_stats': summarize_scores(scores),
                'memory_bank_path': str(bank_path),
                'samples': per_sample,
            }
            write_json(output_root / 'patchcore_degraded' / 'results' / degradation / f'{category}.json', summary)
            category_summary.append({'degradation': degradation, 'image_auc': summary['image_auc']})
            print(f'[{category}][{degradation}] PatchCore image AUC={summary["image_auc"]:.4f}')

        write_json(output_root / 'patchcore_degraded' / 'results' / f'{category}_summary.json', {'category': category, 'items': category_summary})


if __name__ == '__main__':
    main()
