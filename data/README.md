# Data Placeholder

This repository does not redistribute public benchmark datasets.

Download the public datasets from their official sources and place them under:

- `data/eurosat` for EuroSAT
- `data/resisc45` for NWPU-RESISC45
- `data/mvtec` for MVTec AD

Expected layouts:

```text
data/eurosat/<class_name>/*.jpg
data/eurosat/2750/<class_name>/*.jpg
data/resisc45/<class_name>/*.jpg
data/mvtec/<category>/{train,test,ground_truth}/...
```

The released code constructs `EuroSAT-Hard` and `NWPU-Hard` protocols from the
public EuroSAT and NWPU-RESISC45 scene folders at runtime. No separate hard
protocol archive is required.
