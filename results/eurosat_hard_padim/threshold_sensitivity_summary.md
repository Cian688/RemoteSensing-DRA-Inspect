# EuroSAT-Hard PaDiM Matched-FPR and Threshold Sensitivity

Target matched-FPR budget: `0.0536`
Matched-FPR uses one global pooled threshold selected over all EuroSAT-Hard PaDiM test samples.
Global matched-FPR threshold: `0.9800`

## Averaged by Setting

| Setting | Threshold | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- | --- |
| PaDiM-AC (q90) | 0.7409 | 0.1044 | 0.8847 | 0.8884 | 0.8901 |
| PaDiM-AC (q92.5) | 0.8477 | 0.0791 | 0.8431 | 0.8756 | 0.8820 |
| PaDiM-AC (q95) | 1.0000 | 0.0507 | 0.7521 | 0.8311 | 0.8507 |
| PaDiM-AC (matched-FPR) | 0.9800 | 0.0536 | 0.7671 | 0.8427 | 0.8568 |
| PaDiM-AC (q97.5) | 1.2250 | 0.0228 | 0.5989 | 0.7320 | 0.7881 |

## Detailed Results

| Protocol | Degradation | Setting | Threshold | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | PaDiM-AC (q90) | 0.7471 | 0.0867 | 0.8167 | 0.8581 | 0.8650 |
| urban_residential | blur | PaDiM-AC (q92.5) | 0.8456 | 0.0633 | 0.7783 | 0.8452 | 0.8575 |
| urban_residential | blur | PaDiM-AC (q95) | 1.0000 | 0.0333 | 0.6900 | 0.8008 | 0.8283 |
| urban_residential | blur | PaDiM-AC (matched-FPR) | 0.9800 | 0.0350 | 0.7067 | 0.8115 | 0.8358 |
| urban_residential | blur | PaDiM-AC (q97.5) | 1.2358 | 0.0100 | 0.5700 | 0.7215 | 0.7800 |
| urban_residential | jpeg | PaDiM-AC (q90) | 0.7471 | 0.1500 | 0.9167 | 0.8871 | 0.8833 |
| urban_residential | jpeg | PaDiM-AC (q92.5) | 0.8456 | 0.1233 | 0.8917 | 0.8850 | 0.8842 |
| urban_residential | jpeg | PaDiM-AC (q95) | 1.0000 | 0.0850 | 0.8383 | 0.8718 | 0.8767 |
| urban_residential | jpeg | PaDiM-AC (matched-FPR) | 0.9800 | 0.0883 | 0.8517 | 0.8780 | 0.8817 |
| urban_residential | jpeg | PaDiM-AC (q97.5) | 1.2358 | 0.0367 | 0.7183 | 0.8186 | 0.8408 |
| urban_residential | light | PaDiM-AC (q90) | 0.7471 | 0.0400 | 0.7817 | 0.8582 | 0.8708 |
| urban_residential | light | PaDiM-AC (q92.5) | 0.8456 | 0.0350 | 0.7467 | 0.8382 | 0.8558 |
| urban_residential | light | PaDiM-AC (q95) | 1.0000 | 0.0167 | 0.6717 | 0.7957 | 0.8275 |
| urban_residential | light | PaDiM-AC (matched-FPR) | 0.9800 | 0.0183 | 0.6850 | 0.8043 | 0.8333 |
| urban_residential | light | PaDiM-AC (q97.5) | 1.2358 | 0.0100 | 0.5050 | 0.6667 | 0.7475 |
| urban_residential | lowres | PaDiM-AC (q90) | 0.7471 | 0.1167 | 0.8500 | 0.8644 | 0.8667 |
| urban_residential | lowres | PaDiM-AC (q92.5) | 0.8456 | 0.0883 | 0.8133 | 0.8554 | 0.8625 |
| urban_residential | lowres | PaDiM-AC (q95) | 1.0000 | 0.0533 | 0.7483 | 0.8307 | 0.8475 |
| urban_residential | lowres | PaDiM-AC (matched-FPR) | 0.9800 | 0.0583 | 0.7550 | 0.8327 | 0.8483 |
| urban_residential | lowres | PaDiM-AC (q97.5) | 1.2358 | 0.0233 | 0.5983 | 0.7379 | 0.7875 |
| urban_residential | noise | PaDiM-AC (q90) | 0.7471 | 0.1467 | 0.9517 | 0.9071 | 0.9025 |
| urban_residential | noise | PaDiM-AC (q92.5) | 0.8456 | 0.1200 | 0.9317 | 0.9082 | 0.9058 |
| urban_residential | noise | PaDiM-AC (q95) | 1.0000 | 0.0750 | 0.8850 | 0.9031 | 0.9050 |
| urban_residential | noise | PaDiM-AC (matched-FPR) | 0.9800 | 0.0767 | 0.8967 | 0.9088 | 0.9100 |
| urban_residential | noise | PaDiM-AC (q97.5) | 1.2358 | 0.0333 | 0.7717 | 0.8550 | 0.8692 |
| vegetation_forest | blur | PaDiM-AC (q90) | 0.6914 | 0.0533 | 0.8067 | 0.8674 | 0.8767 |
| vegetation_forest | blur | PaDiM-AC (q92.5) | 0.8138 | 0.0367 | 0.7550 | 0.8428 | 0.8592 |
| vegetation_forest | blur | PaDiM-AC (q95) | 1.0000 | 0.0117 | 0.6667 | 0.7944 | 0.8275 |
| vegetation_forest | blur | PaDiM-AC (matched-FPR) | 0.9800 | 0.0117 | 0.6733 | 0.7992 | 0.8308 |
| vegetation_forest | blur | PaDiM-AC (q97.5) | 1.2995 | 0.0017 | 0.5283 | 0.6906 | 0.7633 |
| vegetation_forest | jpeg | PaDiM-AC (q90) | 0.6914 | 0.2200 | 0.8883 | 0.8427 | 0.8342 |
| vegetation_forest | jpeg | PaDiM-AC (q92.5) | 0.8138 | 0.1800 | 0.8583 | 0.8422 | 0.8392 |
| vegetation_forest | jpeg | PaDiM-AC (q95) | 1.0000 | 0.1217 | 0.7800 | 0.8203 | 0.8292 |
| vegetation_forest | jpeg | PaDiM-AC (matched-FPR) | 0.9800 | 0.1283 | 0.7883 | 0.8226 | 0.8300 |
| vegetation_forest | jpeg | PaDiM-AC (q97.5) | 1.2995 | 0.0667 | 0.6683 | 0.7704 | 0.8008 |
| vegetation_forest | light | PaDiM-AC (q90) | 0.6914 | 0.0217 | 0.7683 | 0.8585 | 0.8733 |
| vegetation_forest | light | PaDiM-AC (q92.5) | 0.8138 | 0.0100 | 0.7067 | 0.8233 | 0.8483 |
| vegetation_forest | light | PaDiM-AC (q95) | 1.0000 | 0.0033 | 0.6100 | 0.7562 | 0.8033 |
| vegetation_forest | light | PaDiM-AC (matched-FPR) | 0.9800 | 0.0033 | 0.6200 | 0.7639 | 0.8083 |
| vegetation_forest | light | PaDiM-AC (q97.5) | 1.2995 | 0.0000 | 0.4783 | 0.6471 | 0.7392 |
| vegetation_forest | lowres | PaDiM-AC (q90) | 0.6914 | 0.1183 | 0.8050 | 0.8371 | 0.8433 |
| vegetation_forest | lowres | PaDiM-AC (q92.5) | 0.8138 | 0.0883 | 0.7633 | 0.8245 | 0.8375 |
| vegetation_forest | lowres | PaDiM-AC (q95) | 1.0000 | 0.0567 | 0.6650 | 0.7725 | 0.8042 |
| vegetation_forest | lowres | PaDiM-AC (matched-FPR) | 0.9800 | 0.0617 | 0.6717 | 0.7750 | 0.8050 |
| vegetation_forest | lowres | PaDiM-AC (q97.5) | 1.2995 | 0.0117 | 0.5117 | 0.6718 | 0.7500 |
| vegetation_forest | noise | PaDiM-AC (q90) | 0.6914 | 0.0950 | 0.9350 | 0.9212 | 0.9200 |
| vegetation_forest | noise | PaDiM-AC (q92.5) | 0.8138 | 0.0417 | 0.9033 | 0.9289 | 0.9308 |
| vegetation_forest | noise | PaDiM-AC (q95) | 1.0000 | 0.0200 | 0.8183 | 0.8903 | 0.8992 |
| vegetation_forest | noise | PaDiM-AC (matched-FPR) | 0.9800 | 0.0217 | 0.8283 | 0.8955 | 0.9033 |
| vegetation_forest | noise | PaDiM-AC (q97.5) | 1.2995 | 0.0033 | 0.6583 | 0.7924 | 0.8275 |
| water_sealake | blur | PaDiM-AC (q90) | 0.7842 | 0.0933 | 0.9383 | 0.9237 | 0.9225 |
| water_sealake | blur | PaDiM-AC (q92.5) | 0.8836 | 0.0733 | 0.8567 | 0.8877 | 0.8917 |
| water_sealake | blur | PaDiM-AC (q95) | 1.0000 | 0.0433 | 0.7100 | 0.8099 | 0.8333 |
| water_sealake | blur | PaDiM-AC (matched-FPR) | 0.9800 | 0.0450 | 0.7367 | 0.8269 | 0.8458 |
| water_sealake | blur | PaDiM-AC (q97.5) | 1.1396 | 0.0183 | 0.5067 | 0.6645 | 0.7442 |
| water_sealake | jpeg | PaDiM-AC (q90) | 0.7842 | 0.1167 | 0.9750 | 0.9323 | 0.9292 |
| water_sealake | jpeg | PaDiM-AC (q92.5) | 0.8836 | 0.0983 | 0.9500 | 0.9276 | 0.9258 |
| water_sealake | jpeg | PaDiM-AC (q95) | 1.0000 | 0.0733 | 0.8800 | 0.9010 | 0.9033 |
| water_sealake | jpeg | PaDiM-AC (matched-FPR) | 0.9800 | 0.0783 | 0.8983 | 0.9089 | 0.9100 |
| water_sealake | jpeg | PaDiM-AC (q97.5) | 1.1396 | 0.0467 | 0.7467 | 0.8327 | 0.8500 |
| water_sealake | light | PaDiM-AC (q90) | 0.7842 | 0.0817 | 0.9367 | 0.9282 | 0.9275 |
| water_sealake | light | PaDiM-AC (q92.5) | 0.8836 | 0.0533 | 0.8850 | 0.9132 | 0.9158 |
| water_sealake | light | PaDiM-AC (q95) | 1.0000 | 0.0383 | 0.7133 | 0.8145 | 0.8375 |
| water_sealake | light | PaDiM-AC (matched-FPR) | 0.9800 | 0.0417 | 0.7467 | 0.8350 | 0.8525 |
| water_sealake | light | PaDiM-AC (q97.5) | 1.1396 | 0.0150 | 0.4917 | 0.6527 | 0.7383 |
| water_sealake | lowres | PaDiM-AC (q90) | 0.7842 | 0.0867 | 0.9017 | 0.9070 | 0.9075 |
| water_sealake | lowres | PaDiM-AC (q92.5) | 0.8836 | 0.0583 | 0.8183 | 0.8721 | 0.8800 |
| water_sealake | lowres | PaDiM-AC (q95) | 1.0000 | 0.0383 | 0.6567 | 0.7748 | 0.8092 |
| water_sealake | lowres | PaDiM-AC (matched-FPR) | 0.9800 | 0.0400 | 0.6850 | 0.7942 | 0.8225 |
| water_sealake | lowres | PaDiM-AC (q97.5) | 1.1396 | 0.0150 | 0.4250 | 0.5903 | 0.7050 |
| water_sealake | noise | PaDiM-AC (q90) | 0.7842 | 0.1400 | 0.9983 | 0.9337 | 0.9292 |
| water_sealake | noise | PaDiM-AC (q92.5) | 0.8836 | 0.1167 | 0.9883 | 0.9390 | 0.9358 |
| water_sealake | noise | PaDiM-AC (q95) | 1.0000 | 0.0900 | 0.9483 | 0.9305 | 0.9292 |
| water_sealake | noise | PaDiM-AC (matched-FPR) | 0.9800 | 0.0950 | 0.9633 | 0.9360 | 0.9342 |
| water_sealake | noise | PaDiM-AC (q97.5) | 1.1396 | 0.0500 | 0.8050 | 0.8679 | 0.8775 |

