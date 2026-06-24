# EuroSAT-Hard Calibration Baselines

Matched-FPR diagnostic budget for `q50/q95`: `0.0536`
The matched-FPR row uses one global pooled threshold selected over all mixed-memory samples.
Global matched-FPR threshold: `0.9392`

## Averaged by Setting

| Calibration | Threshold | FPR | TPR | F1 | BAcc | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| Clean-Q95 | 4.1348 | 0.0221 | 0.5056 | 0.6198 | 0.7417 | conservative |
| z-score | 1.0000 | 0.1381 | 0.8630 | 0.8439 | 0.8624 | mean/std normal-score scaling |
| median-IQR | 1.0000 | 0.0847 | 0.7897 | 0.8100 | 0.8525 | robust scaling |
| q50/q95 | 1.0000 | 0.0427 | 0.6546 | 0.7388 | 0.8059 | proposed AC |
| q50/q95 matched-FPR | 0.9392 | 0.0536 | 0.7106 | 0.8056 | 0.8285 | diagnostic |

## Detailed Results

| Protocol | Degradation | Calibration | Threshold | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | Clean-Q95 | 4.3973 | 0.0000 | 0.0967 | 0.1763 | 0.5483 |
| urban_residential | blur | z-score | 1.0000 | 0.0050 | 0.3400 | 0.5056 | 0.6675 |
| urban_residential | blur | median-IQR | 1.0000 | 0.0017 | 0.1883 | 0.3165 | 0.5933 |
| urban_residential | blur | q50/q95 | 1.0000 | 0.0000 | 0.1683 | 0.2882 | 0.5842 |
| urban_residential | blur | q50/q95 matched-FPR | 0.9392 | 0.0017 | 0.1867 | 0.3142 | 0.5925 |
| urban_residential | jpeg | Clean-Q95 | 4.3973 | 0.0667 | 0.6883 | 0.7844 | 0.8108 |
| urban_residential | jpeg | z-score | 1.0000 | 0.3467 | 0.9567 | 0.8307 | 0.8050 |
| urban_residential | jpeg | median-IQR | 1.0000 | 0.1517 | 0.8583 | 0.8541 | 0.8533 |
| urban_residential | jpeg | q50/q95 | 1.0000 | 0.1217 | 0.8183 | 0.8436 | 0.8483 |
| urban_residential | jpeg | q50/q95 matched-FPR | 0.9392 | 0.1483 | 0.8533 | 0.8526 | 0.8525 |
| urban_residential | light | Clean-Q95 | 4.3973 | 0.0133 | 0.4817 | 0.6444 | 0.7342 |
| urban_residential | light | z-score | 1.0000 | 0.1267 | 0.9067 | 0.8918 | 0.8900 |
| urban_residential | light | median-IQR | 1.0000 | 0.0400 | 0.7250 | 0.8215 | 0.8425 |
| urban_residential | light | q50/q95 | 1.0000 | 0.0333 | 0.6867 | 0.7984 | 0.8267 |
| urban_residential | light | q50/q95 matched-FPR | 0.9392 | 0.0400 | 0.7217 | 0.8193 | 0.8408 |
| urban_residential | lowres | Clean-Q95 | 4.3973 | 0.0000 | 0.0800 | 0.1481 | 0.5400 |
| urban_residential | lowres | z-score | 1.0000 | 0.0050 | 0.2967 | 0.4558 | 0.6458 |
| urban_residential | lowres | median-IQR | 1.0000 | 0.0000 | 0.1583 | 0.2734 | 0.5792 |
| urban_residential | lowres | q50/q95 | 1.0000 | 0.0000 | 0.1350 | 0.2379 | 0.5675 |
| urban_residential | lowres | q50/q95 matched-FPR | 0.9392 | 0.0000 | 0.1583 | 0.2734 | 0.5792 |
| urban_residential | noise | Clean-Q95 | 4.3973 | 0.0117 | 0.4800 | 0.6436 | 0.7342 |
| urban_residential | noise | z-score | 1.0000 | 0.1317 | 0.8733 | 0.8712 | 0.8708 |
| urban_residential | noise | median-IQR | 1.0000 | 0.0567 | 0.6700 | 0.7761 | 0.8067 |
| urban_residential | noise | q50/q95 | 1.0000 | 0.0383 | 0.6267 | 0.7528 | 0.7942 |
| urban_residential | noise | q50/q95 matched-FPR | 0.9392 | 0.0567 | 0.6717 | 0.7772 | 0.8075 |
| vegetation_forest | blur | Clean-Q95 | 3.7256 | 0.0000 | 0.5650 | 0.7220 | 0.7825 |
| vegetation_forest | blur | z-score | 1.0000 | 0.0333 | 0.8767 | 0.9180 | 0.9217 |
| vegetation_forest | blur | median-IQR | 1.0000 | 0.0133 | 0.8050 | 0.8854 | 0.8958 |
| vegetation_forest | blur | q50/q95 | 1.0000 | 0.0067 | 0.6833 | 0.8087 | 0.8383 |
| vegetation_forest | blur | q50/q95 matched-FPR | 0.9392 | 0.0067 | 0.7050 | 0.8238 | 0.8492 |
| vegetation_forest | jpeg | Clean-Q95 | 3.7256 | 0.0517 | 0.8583 | 0.8988 | 0.9033 |
| vegetation_forest | jpeg | z-score | 1.0000 | 0.2500 | 0.9733 | 0.8756 | 0.8617 |
| vegetation_forest | jpeg | median-IQR | 1.0000 | 0.1767 | 0.9617 | 0.8995 | 0.8925 |
| vegetation_forest | jpeg | q50/q95 | 1.0000 | 0.0950 | 0.8967 | 0.9004 | 0.9008 |
| vegetation_forest | jpeg | q50/q95 matched-FPR | 0.9392 | 0.1133 | 0.9233 | 0.9067 | 0.9050 |
| vegetation_forest | light | Clean-Q95 | 3.7256 | 0.0267 | 0.8133 | 0.8841 | 0.8933 |
| vegetation_forest | light | z-score | 1.0000 | 0.2083 | 0.9733 | 0.8923 | 0.8825 |
| vegetation_forest | light | median-IQR | 1.0000 | 0.1333 | 0.9383 | 0.9059 | 0.9025 |
| vegetation_forest | light | q50/q95 | 1.0000 | 0.0517 | 0.8767 | 0.9092 | 0.9125 |
| vegetation_forest | light | q50/q95 matched-FPR | 0.9392 | 0.0600 | 0.8917 | 0.9137 | 0.9158 |
| vegetation_forest | lowres | Clean-Q95 | 3.7256 | 0.0000 | 0.5067 | 0.6726 | 0.7533 |
| vegetation_forest | lowres | z-score | 1.0000 | 0.0133 | 0.8150 | 0.8915 | 0.9008 |
| vegetation_forest | lowres | median-IQR | 1.0000 | 0.0100 | 0.7367 | 0.8435 | 0.8633 |
| vegetation_forest | lowres | q50/q95 | 1.0000 | 0.0017 | 0.6000 | 0.7492 | 0.7992 |
| vegetation_forest | lowres | q50/q95 matched-FPR | 0.9392 | 0.0017 | 0.6367 | 0.7772 | 0.8175 |
| vegetation_forest | noise | Clean-Q95 | 3.7256 | 0.0117 | 0.7333 | 0.8405 | 0.8608 |
| vegetation_forest | noise | z-score | 1.0000 | 0.1333 | 0.9350 | 0.9041 | 0.9008 |
| vegetation_forest | noise | median-IQR | 1.0000 | 0.0800 | 0.9000 | 0.9091 | 0.9100 |
| vegetation_forest | noise | q50/q95 | 1.0000 | 0.0283 | 0.8150 | 0.8843 | 0.8933 |
| vegetation_forest | noise | q50/q95 matched-FPR | 0.9392 | 0.0350 | 0.8433 | 0.8980 | 0.9042 |
| water_sealake | blur | Clean-Q95 | 4.2815 | 0.0117 | 0.2267 | 0.3661 | 0.6075 |
| water_sealake | blur | z-score | 1.0000 | 0.1400 | 1.0000 | 0.9346 | 0.9300 |
| water_sealake | blur | median-IQR | 1.0000 | 0.0950 | 0.9650 | 0.9369 | 0.9350 |
| water_sealake | blur | q50/q95 | 1.0000 | 0.0267 | 0.5250 | 0.6767 | 0.7492 |
| water_sealake | blur | q50/q95 matched-FPR | 0.9392 | 0.0350 | 0.6950 | 0.8035 | 0.8300 |
| water_sealake | jpeg | Clean-Q95 | 4.2815 | 0.0567 | 0.7500 | 0.8303 | 0.8467 |
| water_sealake | jpeg | z-score | 1.0000 | 0.2000 | 1.0000 | 0.9091 | 0.9000 |
| water_sealake | jpeg | median-IQR | 1.0000 | 0.1517 | 1.0000 | 0.9295 | 0.9242 |
| water_sealake | jpeg | q50/q95 | 1.0000 | 0.0800 | 0.9167 | 0.9182 | 0.9183 |
| water_sealake | jpeg | q50/q95 matched-FPR | 0.9392 | 0.1033 | 0.9600 | 0.9305 | 0.9283 |
| water_sealake | light | Clean-Q95 | 4.2815 | 0.0350 | 0.6283 | 0.7555 | 0.7967 |
| water_sealake | light | z-score | 1.0000 | 0.1883 | 1.0000 | 0.9139 | 0.9058 |
| water_sealake | light | median-IQR | 1.0000 | 0.1433 | 1.0000 | 0.9331 | 0.9283 |
| water_sealake | light | q50/q95 | 1.0000 | 0.0717 | 0.8883 | 0.9065 | 0.9083 |
| water_sealake | light | q50/q95 matched-FPR | 0.9392 | 0.0867 | 0.9500 | 0.9329 | 0.9317 |
| water_sealake | lowres | Clean-Q95 | 4.2815 | 0.0100 | 0.1500 | 0.2586 | 0.5700 |
| water_sealake | lowres | z-score | 1.0000 | 0.1200 | 0.9983 | 0.9426 | 0.9392 |
| water_sealake | lowres | median-IQR | 1.0000 | 0.0900 | 0.9467 | 0.9296 | 0.9283 |
| water_sealake | lowres | q50/q95 | 1.0000 | 0.0200 | 0.3933 | 0.5566 | 0.6867 |
| water_sealake | lowres | q50/q95 matched-FPR | 0.9392 | 0.0300 | 0.5817 | 0.7218 | 0.7758 |
| water_sealake | noise | Clean-Q95 | 4.2815 | 0.0367 | 0.5250 | 0.6724 | 0.7442 |
| water_sealake | noise | z-score | 1.0000 | 0.1700 | 1.0000 | 0.9217 | 0.9150 |
| water_sealake | noise | median-IQR | 1.0000 | 0.1267 | 0.9917 | 0.9363 | 0.9325 |
| water_sealake | noise | q50/q95 | 1.0000 | 0.0650 | 0.7883 | 0.8507 | 0.8617 |
| water_sealake | noise | q50/q95 matched-FPR | 0.9392 | 0.0850 | 0.8800 | 0.8957 | 0.8975 |

