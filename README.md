# RemoteSensing-DRA-Inspect

Code, configurations, and processed outputs for DRA-Inspect.

## Overview

This repository contains a cleaned public release for scene-level anomaly detection experiments on degraded remote sensing imagery.

Included components:

- experiment configurations
- dataset loading and protocol construction
- synthetic degradation utilities
- memory-based evaluation code
- summary scripts
- processed outputs for reproducibility

## Structure

```text
configs/       experiment configurations
data/          dataset placeholder and expected dataset roots
datasets/      dataset loading and protocol construction
degradations/  synthetic degradation pipeline
memory/        memory-bank implementations
models/        backbone definitions
results/       processed outputs for reproducibility
scripts/       experiment and summary scripts
utils/         configuration, IO, and metric utilities
```

## Environment

```bash
pip install -r requirements.txt
```

Tested with Python 3.10+ and PyTorch.

## Datasets

This repository does not redistribute public benchmark datasets.

Please place the public datasets under:

```text
data/eurosat
data/resisc45
data/mvtec
```

Expected layouts:

```text
data/eurosat/<class_name>/*.jpg
data/eurosat/2750/<class_name>/*.jpg
data/resisc45/<class_name>/*.jpg
data/mvtec/<category>/{train,test,ground_truth}/...
```

Notes:

- Hard remote sensing protocols are constructed by the released code from the public EuroSAT and NWPU-RESISC45 scene folders.
- No separate hard-protocol dataset download is required.
- The EuroSAT loader also supports the common `data/eurosat/2750/<class_name>/...` layout.

## Main Scripts

```bash
bash scripts/run_eurosat_hard_main.sh
bash scripts/run_eurosat_hard_main_multiseed.sh
bash scripts/run_eurosat_hard_equal_size.sh
bash scripts/run_eurosat_hard_padim.sh
bash scripts/run_eurosat_hard_unseen_severity.sh
bash scripts/run_eurosat_hard_unseen_family.sh
bash scripts/run_eurosat_hard_coreset_sensitivity.sh
bash scripts/run_resisc45_hard_extended.sh
bash scripts/run_resisc45_hard_extended_multiseed.sh
```

## Notes

- This repository is intended for reproducibility.
- Public benchmark datasets must be obtained from their original sources.
- Cached files, temporary outputs, and private local paths are excluded from the public release.
