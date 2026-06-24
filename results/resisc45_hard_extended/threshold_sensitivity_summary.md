# NWPU-RESISC45 Hard Matched-FPR and Threshold Sensitivity

Target matched-FPR budget: `0.0438`
Matched-FPR uses one global pooled threshold selected over all mixed-memory NWPU-Hard samples.
Global matched-FPR threshold: `0.9408`
## Averaged by Setting

| Setting | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- |
| PatchCore-AC (q95) | 0.0438 | 0.2890 | 0.4201 | 0.6226 |
| DRA-Inspect-AC (q90) | 0.0829 | 0.4411 | 0.5676 | 0.6791 |
| DRA-Inspect-AC (q92.5) | 0.0633 | 0.3921 | 0.5255 | 0.6644 |
| DRA-Inspect-AC (q95) | 0.0376 | 0.2748 | 0.4044 | 0.6186 |
| DRA-Inspect-AC (matched-FPR) | 0.0438 | 0.3074 | 0.4550 | 0.6318 |
| DRA-Inspect-AC (q97.5) | 0.0229 | 0.1920 | 0.2973 | 0.5846 |

## Detailed Results

| Protocol | Degradation | Setting | Threshold | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| infrastructure_airport | blur | PatchCore-AC (q95) | 1.0000 | 0.0429 | 0.3901 | 0.5446 | 0.6736 |
| infrastructure_airport | blur | DRA-Inspect-AC (q90) | 0.7479 | 0.0429 | 0.4468 | 0.6000 | 0.7020 |
| infrastructure_airport | blur | DRA-Inspect-AC (q92.5) | 0.8048 | 0.0286 | 0.4184 | 0.5784 | 0.6949 |
| infrastructure_airport | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0000 | 0.3121 | 0.4757 | 0.6560 |
| infrastructure_airport | blur | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0071 | 0.3333 | 0.4974 | 0.6631 |
| infrastructure_airport | blur | DRA-Inspect-AC (q97.5) | 1.1405 | 0.0000 | 0.2411 | 0.3886 | 0.6206 |
| infrastructure_airport | jpeg | PatchCore-AC (q95) | 1.0000 | 0.0929 | 0.5532 | 0.6724 | 0.7302 |
| infrastructure_airport | jpeg | DRA-Inspect-AC (q90) | 0.7479 | 0.2000 | 0.6809 | 0.7245 | 0.7404 |
| infrastructure_airport | jpeg | DRA-Inspect-AC (q92.5) | 0.8048 | 0.1714 | 0.6454 | 0.7109 | 0.7370 |
| infrastructure_airport | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.0786 | 0.5532 | 0.6783 | 0.7373 |
| infrastructure_airport | jpeg | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.1143 | 0.5887 | 0.6917 | 0.7372 |
| infrastructure_airport | jpeg | DRA-Inspect-AC (q97.5) | 1.1405 | 0.0500 | 0.5248 | 0.6667 | 0.7374 |
| infrastructure_airport | light | PatchCore-AC (q95) | 1.0000 | 0.0071 | 0.3262 | 0.4894 | 0.6595 |
| infrastructure_airport | light | DRA-Inspect-AC (q90) | 0.7479 | 0.0571 | 0.5248 | 0.6637 | 0.7338 |
| infrastructure_airport | light | DRA-Inspect-AC (q92.5) | 0.8048 | 0.0429 | 0.4823 | 0.6326 | 0.7197 |
| infrastructure_airport | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0071 | 0.3262 | 0.4894 | 0.6595 |
| infrastructure_airport | light | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0143 | 0.3688 | 0.5333 | 0.6773 |
| infrastructure_airport | light | DRA-Inspect-AC (q97.5) | 1.1405 | 0.0000 | 0.2624 | 0.4157 | 0.6312 |
| infrastructure_airport | lowres | PatchCore-AC (q95) | 1.0000 | 0.0357 | 0.4113 | 0.5686 | 0.6878 |
| infrastructure_airport | lowres | DRA-Inspect-AC (q90) | 0.7479 | 0.0357 | 0.4610 | 0.6161 | 0.7126 |
| infrastructure_airport | lowres | DRA-Inspect-AC (q92.5) | 0.8048 | 0.0214 | 0.4113 | 0.5743 | 0.6950 |
| infrastructure_airport | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0071 | 0.2979 | 0.4565 | 0.6454 |
| infrastructure_airport | lowres | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0071 | 0.3333 | 0.4974 | 0.6631 |
| infrastructure_airport | lowres | DRA-Inspect-AC (q97.5) | 1.1405 | 0.0000 | 0.2482 | 0.3977 | 0.6241 |
| infrastructure_airport | noise | PatchCore-AC (q95) | 1.0000 | 0.0643 | 0.5177 | 0.6547 | 0.7267 |
| infrastructure_airport | noise | DRA-Inspect-AC (q90) | 0.7479 | 0.1286 | 0.6383 | 0.7229 | 0.7549 |
| infrastructure_airport | noise | DRA-Inspect-AC (q92.5) | 0.8048 | 0.1000 | 0.5957 | 0.7029 | 0.7479 |
| infrastructure_airport | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0643 | 0.5106 | 0.6486 | 0.7232 |
| infrastructure_airport | noise | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0786 | 0.5319 | 0.6608 | 0.7267 |
| infrastructure_airport | noise | DRA-Inspect-AC (q97.5) | 1.1405 | 0.0429 | 0.4184 | 0.5728 | 0.6878 |
| urban_dense | blur | PatchCore-AC (q95) | 1.0000 | 0.0214 | 0.2000 | 0.3275 | 0.5893 |
| urban_dense | blur | DRA-Inspect-AC (q90) | 0.7514 | 0.0214 | 0.2214 | 0.3563 | 0.6000 |
| urban_dense | blur | DRA-Inspect-AC (q92.5) | 0.8642 | 0.0143 | 0.1929 | 0.3195 | 0.5893 |
| urban_dense | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0143 | 0.1357 | 0.2360 | 0.5607 |
| urban_dense | blur | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0143 | 0.1714 | 0.2892 | 0.5786 |
| urban_dense | blur | DRA-Inspect-AC (q97.5) | 1.1472 | 0.0071 | 0.0786 | 0.1447 | 0.5357 |
| urban_dense | jpeg | PatchCore-AC (q95) | 1.0000 | 0.0643 | 0.3071 | 0.4479 | 0.6214 |
| urban_dense | jpeg | DRA-Inspect-AC (q90) | 0.7514 | 0.1500 | 0.5143 | 0.6180 | 0.6821 |
| urban_dense | jpeg | DRA-Inspect-AC (q92.5) | 0.8642 | 0.1214 | 0.4786 | 0.5982 | 0.6786 |
| urban_dense | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.0857 | 0.3571 | 0.4950 | 0.6357 |
| urban_dense | jpeg | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0929 | 0.3857 | 0.5217 | 0.6464 |
| urban_dense | jpeg | DRA-Inspect-AC (q97.5) | 1.1472 | 0.0500 | 0.2643 | 0.4022 | 0.6071 |
| urban_dense | light | PatchCore-AC (q95) | 1.0000 | 0.0214 | 0.1286 | 0.2236 | 0.5536 |
| urban_dense | light | DRA-Inspect-AC (q90) | 0.7514 | 0.0286 | 0.2714 | 0.4176 | 0.6214 |
| urban_dense | light | DRA-Inspect-AC (q92.5) | 0.8642 | 0.0214 | 0.2214 | 0.3563 | 0.6000 |
| urban_dense | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0214 | 0.1429 | 0.2454 | 0.5607 |
| urban_dense | light | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0214 | 0.1714 | 0.2874 | 0.5750 |
| urban_dense | light | DRA-Inspect-AC (q97.5) | 1.1472 | 0.0071 | 0.0857 | 0.1569 | 0.5393 |
| urban_dense | lowres | PatchCore-AC (q95) | 1.0000 | 0.0357 | 0.2000 | 0.3237 | 0.5821 |
| urban_dense | lowres | DRA-Inspect-AC (q90) | 0.7514 | 0.0214 | 0.2357 | 0.3750 | 0.6071 |
| urban_dense | lowres | DRA-Inspect-AC (q92.5) | 0.8642 | 0.0143 | 0.1786 | 0.2994 | 0.5821 |
| urban_dense | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0143 | 0.1286 | 0.2250 | 0.5571 |
| urban_dense | lowres | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0143 | 0.1429 | 0.2469 | 0.5643 |
| urban_dense | lowres | DRA-Inspect-AC (q97.5) | 1.1472 | 0.0071 | 0.0857 | 0.1569 | 0.5393 |
| urban_dense | noise | PatchCore-AC (q95) | 1.0000 | 0.0429 | 0.2214 | 0.3503 | 0.5893 |
| urban_dense | noise | DRA-Inspect-AC (q90) | 0.7514 | 0.0929 | 0.4429 | 0.5767 | 0.6750 |
| urban_dense | noise | DRA-Inspect-AC (q92.5) | 0.8642 | 0.0500 | 0.3500 | 0.5000 | 0.6500 |
| urban_dense | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0429 | 0.2429 | 0.3778 | 0.6000 |
| urban_dense | noise | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0429 | 0.2929 | 0.4385 | 0.6250 |
| urban_dense | noise | DRA-Inspect-AC (q97.5) | 1.1472 | 0.0214 | 0.1857 | 0.3077 | 0.5821 |
| vegetation_forest | blur | PatchCore-AC (q95) | 1.0000 | 0.0429 | 0.2214 | 0.3503 | 0.5893 |
| vegetation_forest | blur | DRA-Inspect-AC (q90) | 0.7347 | 0.0857 | 0.3929 | 0.5314 | 0.6536 |
| vegetation_forest | blur | DRA-Inspect-AC (q92.5) | 0.8078 | 0.0571 | 0.3214 | 0.4663 | 0.6321 |
| vegetation_forest | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0357 | 0.1786 | 0.2941 | 0.5714 |
| vegetation_forest | blur | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0429 | 0.2000 | 0.3218 | 0.5786 |
| vegetation_forest | blur | DRA-Inspect-AC (q97.5) | 1.2241 | 0.0286 | 0.0571 | 0.1053 | 0.5143 |
| vegetation_forest | jpeg | PatchCore-AC (q95) | 1.0000 | 0.0500 | 0.2929 | 0.4362 | 0.6214 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q90) | 0.7347 | 0.1143 | 0.5214 | 0.6376 | 0.7036 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q92.5) | 0.8078 | 0.1000 | 0.4786 | 0.6063 | 0.6893 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.0571 | 0.3357 | 0.4821 | 0.6393 |
| vegetation_forest | jpeg | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0714 | 0.3929 | 0.5366 | 0.6607 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q97.5) | 1.2241 | 0.0429 | 0.1643 | 0.2722 | 0.5607 |
| vegetation_forest | light | PatchCore-AC (q95) | 1.0000 | 0.0429 | 0.1571 | 0.2619 | 0.5571 |
| vegetation_forest | light | DRA-Inspect-AC (q90) | 0.7347 | 0.0786 | 0.4143 | 0.5550 | 0.6679 |
| vegetation_forest | light | DRA-Inspect-AC (q92.5) | 0.8078 | 0.0714 | 0.3357 | 0.4772 | 0.6321 |
| vegetation_forest | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0500 | 0.1857 | 0.3006 | 0.5679 |
| vegetation_forest | light | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0500 | 0.2286 | 0.3575 | 0.5893 |
| vegetation_forest | light | DRA-Inspect-AC (q97.5) | 1.2241 | 0.0286 | 0.0786 | 0.1419 | 0.5250 |
| vegetation_forest | lowres | PatchCore-AC (q95) | 1.0000 | 0.0429 | 0.2214 | 0.3503 | 0.5893 |
| vegetation_forest | lowres | DRA-Inspect-AC (q90) | 0.7347 | 0.0929 | 0.4143 | 0.5498 | 0.6607 |
| vegetation_forest | lowres | DRA-Inspect-AC (q92.5) | 0.8078 | 0.0643 | 0.3500 | 0.4949 | 0.6429 |
| vegetation_forest | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0357 | 0.1786 | 0.2941 | 0.5714 |
| vegetation_forest | lowres | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0357 | 0.2000 | 0.3237 | 0.5821 |
| vegetation_forest | lowres | DRA-Inspect-AC (q97.5) | 1.2241 | 0.0214 | 0.0786 | 0.1429 | 0.5286 |
| vegetation_forest | noise | PatchCore-AC (q95) | 1.0000 | 0.0500 | 0.1857 | 0.3006 | 0.5679 |
| vegetation_forest | noise | DRA-Inspect-AC (q90) | 0.7347 | 0.0929 | 0.4357 | 0.5701 | 0.6714 |
| vegetation_forest | noise | DRA-Inspect-AC (q92.5) | 0.8078 | 0.0714 | 0.4214 | 0.5646 | 0.6750 |
| vegetation_forest | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0500 | 0.2357 | 0.3667 | 0.5929 |
| vegetation_forest | noise | DRA-Inspect-AC (matched-FPR) | 0.9408 | 0.0500 | 0.2643 | 0.4022 | 0.6071 |
| vegetation_forest | noise | DRA-Inspect-AC (q97.5) | 1.2241 | 0.0357 | 0.1071 | 0.1875 | 0.5357 |

