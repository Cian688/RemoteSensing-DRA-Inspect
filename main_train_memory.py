from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from datasets import collect_mvtec_samples
from degradations import generate_variants
from memory import DegradationMemoryBank
from models import SimplePatchBackbone
from utils.config import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Build DRA-Inspect multi-degradation memory bank.')
    parser.add_argument('--config', type=str, required=True, help='Path to YAML config file.')
    parser.add_argument('--category', type=str, default=None, help='Single MVTec category override.')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    dataset_root = config['dataset']['root']
    categories = [args.category] if args.category else list(config['dataset']['categories'])
    degradation_names = list(config['degradations']['train'])
    severity = float(config['degradations'].get('severity', 1.0))
    output_root = Path(config['output']['root'])
    backbone = SimplePatchBackbone(
        image_size=int(config['feature_extractor']['image_size']),
        patch_size=int(config['feature_extractor']['patch_size']),
    )

    for category in categories:
        samples = collect_mvtec_samples(dataset_root, category=category, split='train')
        good_samples = [sample for sample in samples if sample.label == 'good']
        bank = DegradationMemoryBank()
        for sample in tqdm(good_samples, desc=f'Building bank for {category}'):
            image = Image.open(sample.image_path).convert('RGB')
            variants = generate_variants(image, degradation_names, severity=severity)
            for name, degraded_image in variants.items():
                features = backbone.extract(degraded_image).features
                bank.add(name, features)
        bank.finalize()
        save_path = output_root / 'banks' / f'{category}_memory.npz'
        bank.save(save_path)
        print(f'Saved memory bank for {category}: {save_path}')


if __name__ == '__main__':
    main()
