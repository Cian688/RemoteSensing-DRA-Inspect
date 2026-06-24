# RemoteSensing-DRA-Inspect

Code, configurations, and processed result files for the paper:

`DRA-Inspect: Reliability-Calibrated Memory-Based Anomaly Detection for Degraded Remote Sensing Imagery`

## Overview

This repository contains the core code used for the remote sensing experiments in the paper, together with the processed result files used to generate the reported tables and appendix summaries.

The repository focuses on:

- EuroSAT-Hard main evaluation
- NWPU-Hard extended evaluation
- PaDiM comparison on EuroSAT-Hard
- multi-seed stability
- bootstrap confidence intervals
- equal-size memory control
- unseen severity and unseen family transfer
- coreset-ratio sensitivity
- approximate retrieval diagnostics

## Repository Structure

```text
configs/       experiment configurations
data/          dataset placeholder and expected dataset roots
datasets/      dataset loading and protocol construction
degradations/  synthetic degradation pipeline
docs/          manuscript files used for the submitted paper
memory/        memory-bank implementations
models/        backbone definitions
results/       processed result files used in the paper
scripts/       experiment and summary scripts
utils/         configuration, IO, and metric utilities
```

## Environment

Install the minimum dependencies with:

```bash
pip install -r requirements.txt
```

The project was developed with Python 3.10+ and PyTorch.

## Datasets

This repository does not redistribute public benchmark datasets.

Please download the public datasets from their official sources and prepare them under:

```text
data/eurosat
data/resisc45
data/mvtec
```

Expected layouts:

```text
data/eurosat/
  AnnualCrop/
  Forest/
  ...
```

```text
data/resisc45/
  airplane/
  airport/
  ...
```

```text
data/mvtec/
  bottle/
    train/
    test/
    ground_truth/
  ...
```

The main remote sensing configuration file is:

```text
configs/patchcore_remote_sensing.yaml
```

It expects:

- `data/eurosat` for EuroSAT
- `data/resisc45` for NWPU-RESISC45
- `data/mvtec` for MVTec AD

Notes:

- `EuroSAT-Hard` and `NWPU-Hard` are protocol constructions created by this code from the public EuroSAT and NWPU-RESISC45 scene folders; no separate hard-protocol dataset download is required.
- The EuroSAT loader also supports the common `data/eurosat/2750/<class_name>/...` layout shipped by some public mirrors.
- The repository uses repo-relative dataset roots in the released YAML files so the examples work directly after placing the datasets under `data/`.

## Main Reproduction Scripts

Representative experiment entry points:

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

Representative summary scripts:

```bash
python scripts/summarize_eurosat_hard_main.py
python scripts/summarize_eurosat_hard_multiseed.py
python scripts/summarize_eurosat_hard_calibration_baselines.py
python scripts/summarize_eurosat_hard_equal_size.py
python scripts/summarize_eurosat_hard_padim.py
python scripts/summarize_eurosat_hard_unseen_severity.py
python scripts/summarize_eurosat_hard_unseen_family.py
python scripts/summarize_eurosat_hard_coreset_sensitivity.py
python scripts/summarize_resisc45_hard_main.py
python scripts/summarize_resisc45_hard_appendix.py
```

## Processed Results

The final processed result files used in the paper are stored under `results/`.

Key processed outputs included in this release:

- EuroSAT-Hard main summaries
- calibration baseline summaries
- bootstrap summaries
- multi-seed summaries
- equal-size memory summaries
- PaDiM summaries
- unseen severity and unseen family summaries
- coreset-ratio summaries
- ANN retrieval summaries
- NWPU-Hard extended summaries and appendix tables

## Manuscript Files

The submitted manuscript files are stored in `docs/`.

## Notes

- This repository is a cleaned public release intended for paper reproducibility.
- Public benchmark datasets must be obtained from their original sources.
- Runtime logs, temporary outputs, and private local paths from the original development environment are intentionally omitted from this release.
