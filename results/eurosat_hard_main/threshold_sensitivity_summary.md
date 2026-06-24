# EuroSAT-Hard Matched-FPR and Threshold Sensitivity

Target matched-FPR budget: `0.0536`
Matched-FPR uses one global pooled threshold selected over all mixed-memory EuroSAT-Hard samples.
Global matched-FPR threshold: `0.9392`

## Averaged by Setting

| Setting | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- |
| PatchCore-AC (q95) | 0.0536 | 0.7261 | 0.8122 | 0.8363 |
| DRA-Inspect-AC (q90) | 0.0842 | 0.7989 | 0.8236 | 0.8573 |
| DRA-Inspect-AC (q92.5) | 0.0651 | 0.7532 | 0.8014 | 0.8441 |
| DRA-Inspect-AC (q95) | 0.0427 | 0.6546 | 0.7388 | 0.8059 |
| DRA-Inspect-AC (matched-FPR) | 0.0536 | 0.7106 | 0.8056 | 0.8285 |
| DRA-Inspect-AC (q97.5) | 0.0221 | 0.5050 | 0.6196 | 0.7414 |

## Detailed Results

| Protocol | Degradation | Setting | Threshold | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | PatchCore-AC (q95) | 1.0000 | 0.0500 | 0.6567 | 0.7695 | 0.8033 |
| urban_residential | blur | DRA-Inspect-AC (q90) | 0.7934 | 0.0017 | 0.2567 | 0.4079 | 0.6275 |
| urban_residential | blur | DRA-Inspect-AC (q92.5) | 0.8685 | 0.0017 | 0.2167 | 0.3557 | 0.6075 |
| urban_residential | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0000 | 0.1683 | 0.2882 | 0.5842 |
| urban_residential | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0000 | 0.1683 | 0.2882 | 0.5842 |
| urban_residential | blur | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0017 | 0.1867 | 0.3142 | 0.5925 |
| urban_residential | blur | DRA-Inspect-AC (q97.5) | 1.2039 | 0.0000 | 0.0967 | 0.1763 | 0.5483 |
| urban_residential | jpeg | PatchCore-AC (q95) | 1.0000 | 0.1083 | 0.7983 | 0.8374 | 0.8450 |
| urban_residential | jpeg | DRA-Inspect-AC (q90) | 0.7934 | 0.2333 | 0.9100 | 0.8491 | 0.8383 |
| urban_residential | jpeg | DRA-Inspect-AC (q92.5) | 0.8685 | 0.1817 | 0.8850 | 0.8565 | 0.8517 |
| urban_residential | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.1217 | 0.8183 | 0.8436 | 0.8483 |
| urban_residential | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.1217 | 0.8183 | 0.8436 | 0.8483 |
| urban_residential | jpeg | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.1483 | 0.8533 | 0.8526 | 0.8525 |
| urban_residential | jpeg | DRA-Inspect-AC (q97.5) | 1.2039 | 0.0667 | 0.6883 | 0.7844 | 0.8108 |
| urban_residential | light | PatchCore-AC (q95) | 1.0000 | 0.0167 | 0.5450 | 0.6980 | 0.7642 |
| urban_residential | light | DRA-Inspect-AC (q90) | 0.7934 | 0.0617 | 0.8133 | 0.8676 | 0.8758 |
| urban_residential | light | DRA-Inspect-AC (q92.5) | 0.8685 | 0.0550 | 0.7683 | 0.8428 | 0.8567 |
| urban_residential | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0333 | 0.6867 | 0.7984 | 0.8267 |
| urban_residential | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0333 | 0.6867 | 0.7984 | 0.8267 |
| urban_residential | light | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0400 | 0.7217 | 0.8193 | 0.8408 |
| urban_residential | light | DRA-Inspect-AC (q97.5) | 1.2039 | 0.0133 | 0.4950 | 0.6564 | 0.7408 |
| urban_residential | lowres | PatchCore-AC (q95) | 1.0000 | 0.0683 | 0.7167 | 0.8030 | 0.8242 |
| urban_residential | lowres | DRA-Inspect-AC (q90) | 0.7934 | 0.0000 | 0.2100 | 0.3471 | 0.6050 |
| urban_residential | lowres | DRA-Inspect-AC (q92.5) | 0.8685 | 0.0000 | 0.1867 | 0.3146 | 0.5933 |
| urban_residential | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0000 | 0.1350 | 0.2379 | 0.5675 |
| urban_residential | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0000 | 0.1350 | 0.2379 | 0.5675 |
| urban_residential | lowres | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0000 | 0.1583 | 0.2734 | 0.5792 |
| urban_residential | lowres | DRA-Inspect-AC (q97.5) | 1.2039 | 0.0000 | 0.0850 | 0.1567 | 0.5425 |
| urban_residential | noise | PatchCore-AC (q95) | 1.0000 | 0.0267 | 0.5700 | 0.7140 | 0.7717 |
| urban_residential | noise | DRA-Inspect-AC (q90) | 0.7934 | 0.0750 | 0.7867 | 0.8451 | 0.8558 |
| urban_residential | noise | DRA-Inspect-AC (q92.5) | 0.8685 | 0.0667 | 0.7367 | 0.8170 | 0.8350 |
| urban_residential | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0383 | 0.6267 | 0.7528 | 0.7942 |
| urban_residential | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0383 | 0.6267 | 0.7528 | 0.7942 |
| urban_residential | noise | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0567 | 0.6717 | 0.7772 | 0.8075 |
| urban_residential | noise | DRA-Inspect-AC (q97.5) | 1.2039 | 0.0133 | 0.4850 | 0.6474 | 0.7358 |
| vegetation_forest | blur | PatchCore-AC (q95) | 1.0000 | 0.0400 | 0.8367 | 0.8917 | 0.8983 |
| vegetation_forest | blur | DRA-Inspect-AC (q90) | 0.7574 | 0.0133 | 0.8100 | 0.8885 | 0.8983 |
| vegetation_forest | blur | DRA-Inspect-AC (q92.5) | 0.8636 | 0.0083 | 0.7550 | 0.8563 | 0.8733 |
| vegetation_forest | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0067 | 0.6833 | 0.8087 | 0.8383 |
| vegetation_forest | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0067 | 0.6833 | 0.8087 | 0.8383 |
| vegetation_forest | blur | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0067 | 0.7050 | 0.8238 | 0.8492 |
| vegetation_forest | blur | DRA-Inspect-AC (q97.5) | 1.1643 | 0.0000 | 0.5683 | 0.7248 | 0.7842 |
| vegetation_forest | jpeg | PatchCore-AC (q95) | 1.0000 | 0.1317 | 0.8833 | 0.8768 | 0.8758 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q90) | 0.7574 | 0.1817 | 0.9617 | 0.8974 | 0.8900 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q92.5) | 0.8636 | 0.1367 | 0.9383 | 0.9044 | 0.9008 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.0950 | 0.8967 | 0.9004 | 0.9008 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.0950 | 0.8967 | 0.9004 | 0.9008 |
| vegetation_forest | jpeg | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.1133 | 0.9233 | 0.9067 | 0.9050 |
| vegetation_forest | jpeg | DRA-Inspect-AC (q97.5) | 1.1643 | 0.0517 | 0.8583 | 0.8988 | 0.9033 |
| vegetation_forest | light | PatchCore-AC (q95) | 1.0000 | 0.0217 | 0.7683 | 0.8585 | 0.8733 |
| vegetation_forest | light | DRA-Inspect-AC (q90) | 0.7574 | 0.1333 | 0.9383 | 0.9059 | 0.9025 |
| vegetation_forest | light | DRA-Inspect-AC (q92.5) | 0.8636 | 0.0833 | 0.9183 | 0.9176 | 0.9175 |
| vegetation_forest | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0517 | 0.8767 | 0.9092 | 0.9125 |
| vegetation_forest | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0517 | 0.8767 | 0.9092 | 0.9125 |
| vegetation_forest | light | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0600 | 0.8917 | 0.9137 | 0.9158 |
| vegetation_forest | light | DRA-Inspect-AC (q97.5) | 1.1643 | 0.0267 | 0.8133 | 0.8841 | 0.8933 |
| vegetation_forest | lowres | PatchCore-AC (q95) | 1.0000 | 0.0517 | 0.8250 | 0.8792 | 0.8867 |
| vegetation_forest | lowres | DRA-Inspect-AC (q90) | 0.7574 | 0.0100 | 0.7367 | 0.8435 | 0.8633 |
| vegetation_forest | lowres | DRA-Inspect-AC (q92.5) | 0.8636 | 0.0083 | 0.6867 | 0.8102 | 0.8392 |
| vegetation_forest | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0017 | 0.6000 | 0.7492 | 0.7992 |
| vegetation_forest | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0017 | 0.6000 | 0.7492 | 0.7992 |
| vegetation_forest | lowres | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0017 | 0.6367 | 0.7772 | 0.8175 |
| vegetation_forest | lowres | DRA-Inspect-AC (q97.5) | 1.1643 | 0.0000 | 0.5067 | 0.6726 | 0.7533 |
| vegetation_forest | noise | PatchCore-AC (q95) | 1.0000 | 0.0133 | 0.7533 | 0.8528 | 0.8700 |
| vegetation_forest | noise | DRA-Inspect-AC (q90) | 0.7574 | 0.0800 | 0.9017 | 0.9100 | 0.9108 |
| vegetation_forest | noise | DRA-Inspect-AC (q92.5) | 0.8636 | 0.0433 | 0.8683 | 0.9085 | 0.9125 |
| vegetation_forest | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0283 | 0.8150 | 0.8843 | 0.8933 |
| vegetation_forest | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0283 | 0.8150 | 0.8843 | 0.8933 |
| vegetation_forest | noise | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0350 | 0.8433 | 0.8980 | 0.9042 |
| vegetation_forest | noise | DRA-Inspect-AC (q97.5) | 1.1643 | 0.0117 | 0.7333 | 0.8405 | 0.8608 |
| water_sealake | blur | PatchCore-AC (q95) | 1.0000 | 0.0433 | 0.6400 | 0.7604 | 0.7983 |
| water_sealake | blur | DRA-Inspect-AC (q90) | 0.8365 | 0.0700 | 0.8967 | 0.9119 | 0.9133 |
| water_sealake | blur | DRA-Inspect-AC (q92.5) | 0.8972 | 0.0483 | 0.7800 | 0.8532 | 0.8658 |
| water_sealake | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0267 | 0.5250 | 0.6767 | 0.7492 |
| water_sealake | blur | DRA-Inspect-AC (q95) | 1.0000 | 0.0267 | 0.5250 | 0.6767 | 0.7492 |
| water_sealake | blur | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0350 | 0.6950 | 0.8035 | 0.8300 |
| water_sealake | blur | DRA-Inspect-AC (q97.5) | 1.1202 | 0.0117 | 0.2217 | 0.3595 | 0.6050 |
| water_sealake | jpeg | PatchCore-AC (q95) | 1.0000 | 0.0783 | 0.8483 | 0.8806 | 0.8850 |
| water_sealake | jpeg | DRA-Inspect-AC (q90) | 0.8365 | 0.1300 | 0.9933 | 0.9356 | 0.9317 |
| water_sealake | jpeg | DRA-Inspect-AC (q92.5) | 0.8972 | 0.1117 | 0.9800 | 0.9371 | 0.9342 |
| water_sealake | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.0800 | 0.9167 | 0.9182 | 0.9183 |
| water_sealake | jpeg | DRA-Inspect-AC (q95) | 1.0000 | 0.0800 | 0.9167 | 0.9182 | 0.9183 |
| water_sealake | jpeg | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.1033 | 0.9600 | 0.9305 | 0.9283 |
| water_sealake | jpeg | DRA-Inspect-AC (q97.5) | 1.1202 | 0.0567 | 0.7383 | 0.8227 | 0.8408 |
| water_sealake | light | PatchCore-AC (q95) | 1.0000 | 0.0517 | 0.7133 | 0.8083 | 0.8308 |
| water_sealake | light | DRA-Inspect-AC (q90) | 0.8365 | 0.1183 | 0.9933 | 0.9408 | 0.9375 |
| water_sealake | light | DRA-Inspect-AC (q92.5) | 0.8972 | 0.1033 | 0.9717 | 0.9365 | 0.9342 |
| water_sealake | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0717 | 0.8883 | 0.9065 | 0.9083 |
| water_sealake | light | DRA-Inspect-AC (q95) | 1.0000 | 0.0717 | 0.8883 | 0.9065 | 0.9083 |
| water_sealake | light | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0867 | 0.9500 | 0.9329 | 0.9317 |
| water_sealake | light | DRA-Inspect-AC (q97.5) | 1.1202 | 0.0333 | 0.6217 | 0.7513 | 0.7942 |
| water_sealake | lowres | PatchCore-AC (q95) | 1.0000 | 0.0433 | 0.6117 | 0.7392 | 0.7842 |
| water_sealake | lowres | DRA-Inspect-AC (q90) | 0.8365 | 0.0533 | 0.8133 | 0.8714 | 0.8800 |
| water_sealake | lowres | DRA-Inspect-AC (q92.5) | 0.8972 | 0.0367 | 0.6817 | 0.7934 | 0.8225 |
| water_sealake | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0200 | 0.3933 | 0.5566 | 0.6867 |
| water_sealake | lowres | DRA-Inspect-AC (q95) | 1.0000 | 0.0200 | 0.3933 | 0.5566 | 0.6867 |
| water_sealake | lowres | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0300 | 0.5817 | 0.7218 | 0.7758 |
| water_sealake | lowres | DRA-Inspect-AC (q97.5) | 1.1202 | 0.0100 | 0.1467 | 0.2536 | 0.5683 |
| water_sealake | noise | PatchCore-AC (q95) | 1.0000 | 0.0583 | 0.7250 | 0.8131 | 0.8333 |
| water_sealake | noise | DRA-Inspect-AC (q90) | 0.8365 | 0.1017 | 0.9617 | 0.9321 | 0.9300 |
| water_sealake | noise | DRA-Inspect-AC (q92.5) | 0.8972 | 0.0917 | 0.9250 | 0.9174 | 0.9167 |
| water_sealake | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0650 | 0.7883 | 0.8507 | 0.8617 |
| water_sealake | noise | DRA-Inspect-AC (q95) | 1.0000 | 0.0650 | 0.7883 | 0.8507 | 0.8617 |
| water_sealake | noise | DRA-Inspect-AC (matched-FPR) | 0.9392 | 0.0850 | 0.8800 | 0.8957 | 0.8975 |
| water_sealake | noise | DRA-Inspect-AC (q97.5) | 1.1202 | 0.0367 | 0.5167 | 0.6652 | 0.7400 |

