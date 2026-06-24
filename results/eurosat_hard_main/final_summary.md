# EuroSAT-Hard Main Summary

## Protocol-Wise Results

| Protocol | Degradation | Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | PatchCore-CF | 0.9451 | 0.4677 | 0.0533 | 0.6950 | 0.7950 | 0.8208 |
| urban_residential | blur | PatchCore-AC | 0.9451 | 1.2387 | 0.0500 | 0.6567 | 0.7695 | 0.8033 |
| urban_residential | blur | DRA-Inspect-CF | 0.9497 | 0.5255 | 0.0000 | 0.0967 | 0.1763 | 0.5483 |
| urban_residential | blur | DRA-Inspect-AC | 0.9497 | 1.0795 | 0.0000 | 0.1683 | 0.2882 | 0.5842 |
| urban_residential | jpeg | PatchCore-CF | 0.9364 | 0.4654 | 0.1150 | 0.8167 | 0.8456 | 0.8508 |
| urban_residential | jpeg | PatchCore-AC | 0.9364 | 1.2419 | 0.1083 | 0.7983 | 0.8374 | 0.8450 |
| urban_residential | jpeg | DRA-Inspect-CF | 0.9278 | 0.4818 | 0.0667 | 0.6883 | 0.7844 | 0.8108 |
| urban_residential | jpeg | DRA-Inspect-AC | 0.9278 | 0.9877 | 0.1217 | 0.8183 | 0.8436 | 0.8483 |
| urban_residential | light | PatchCore-CF | 0.9596 | 0.5320 | 0.0167 | 0.5783 | 0.7252 | 0.7808 |
| urban_residential | light | PatchCore-AC | 0.9596 | 1.4027 | 0.0167 | 0.5450 | 0.6980 | 0.7642 |
| urban_residential | light | DRA-Inspect-CF | 0.9568 | 0.5242 | 0.0133 | 0.4817 | 0.6444 | 0.7342 |
| urban_residential | light | DRA-Inspect-AC | 0.9568 | 1.0786 | 0.0333 | 0.6867 | 0.7984 | 0.8267 |
| urban_residential | lowres | PatchCore-CF | 0.9408 | 0.4583 | 0.0767 | 0.7450 | 0.8179 | 0.8342 |
| urban_residential | lowres | PatchCore-AC | 0.9408 | 1.2080 | 0.0683 | 0.7167 | 0.8030 | 0.8242 |
| urban_residential | lowres | DRA-Inspect-CF | 0.9472 | 0.5283 | 0.0000 | 0.0800 | 0.1481 | 0.5400 |
| urban_residential | lowres | DRA-Inspect-AC | 0.9472 | 1.0893 | 0.0000 | 0.1350 | 0.2379 | 0.5675 |
| urban_residential | noise | PatchCore-CF | 0.9428 | 0.4913 | 0.0317 | 0.6017 | 0.7367 | 0.7850 |
| urban_residential | noise | PatchCore-AC | 0.9428 | 1.2986 | 0.0267 | 0.5700 | 0.7140 | 0.7717 |
| urban_residential | noise | DRA-Inspect-CF | 0.9380 | 0.5111 | 0.0117 | 0.4800 | 0.6436 | 0.7342 |
| urban_residential | noise | DRA-Inspect-AC | 0.9380 | 1.0545 | 0.0383 | 0.6267 | 0.7528 | 0.7942 |
| vegetation_forest | blur | PatchCore-CF | 0.9742 | 0.9732 | 0.0600 | 0.8633 | 0.8977 | 0.9017 |
| vegetation_forest | blur | PatchCore-AC | 0.9742 | 1.7815 | 0.0400 | 0.8367 | 0.8917 | 0.8983 |
| vegetation_forest | blur | DRA-Inspect-CF | 0.9816 | 1.2273 | 0.0000 | 0.5650 | 0.7220 | 0.7825 |
| vegetation_forest | blur | DRA-Inspect-AC | 0.9816 | 1.8014 | 0.0067 | 0.6833 | 0.8087 | 0.8383 |
| vegetation_forest | jpeg | PatchCore-CF | 0.9546 | 0.8364 | 0.1800 | 0.9083 | 0.8699 | 0.8642 |
| vegetation_forest | jpeg | PatchCore-AC | 0.9546 | 1.5391 | 0.1317 | 0.8833 | 0.8768 | 0.8758 |
| vegetation_forest | jpeg | DRA-Inspect-CF | 0.9719 | 1.1501 | 0.0517 | 0.8583 | 0.8988 | 0.9033 |
| vegetation_forest | jpeg | DRA-Inspect-AC | 0.9719 | 1.6781 | 0.0950 | 0.8967 | 0.9004 | 0.9008 |
| vegetation_forest | light | PatchCore-CF | 0.9733 | 0.9916 | 0.0283 | 0.7967 | 0.8731 | 0.8842 |
| vegetation_forest | light | PatchCore-AC | 0.9733 | 1.8132 | 0.0217 | 0.7683 | 0.8585 | 0.8733 |
| vegetation_forest | light | DRA-Inspect-CF | 0.9760 | 1.0230 | 0.0267 | 0.8133 | 0.8841 | 0.8933 |
| vegetation_forest | light | DRA-Inspect-AC | 0.9760 | 1.4967 | 0.0517 | 0.8767 | 0.9092 | 0.9125 |
| vegetation_forest | lowres | PatchCore-CF | 0.9703 | 0.9498 | 0.0700 | 0.8667 | 0.8950 | 0.8983 |
| vegetation_forest | lowres | PatchCore-AC | 0.9703 | 1.7259 | 0.0517 | 0.8250 | 0.8792 | 0.8867 |
| vegetation_forest | lowres | DRA-Inspect-CF | 0.9803 | 1.2810 | 0.0000 | 0.5067 | 0.6726 | 0.7533 |
| vegetation_forest | lowres | DRA-Inspect-AC | 0.9803 | 1.8757 | 0.0017 | 0.6000 | 0.7492 | 0.7992 |
| vegetation_forest | noise | PatchCore-CF | 0.9726 | 0.9187 | 0.0217 | 0.7833 | 0.8680 | 0.8808 |
| vegetation_forest | noise | PatchCore-AC | 0.9726 | 1.6766 | 0.0133 | 0.7533 | 0.8528 | 0.8700 |
| vegetation_forest | noise | DRA-Inspect-CF | 0.9718 | 1.0667 | 0.0117 | 0.7333 | 0.8405 | 0.8608 |
| vegetation_forest | noise | DRA-Inspect-AC | 0.9718 | 1.5564 | 0.0283 | 0.8150 | 0.8843 | 0.8933 |
| water_sealake | blur | PatchCore-CF | 0.9587 | 1.7933 | 0.0333 | 0.5333 | 0.6809 | 0.7500 |
| water_sealake | blur | PatchCore-AC | 0.9587 | 1.1505 | 0.0433 | 0.6400 | 0.7604 | 0.7983 |
| water_sealake | blur | DRA-Inspect-CF | 0.9683 | 2.0014 | 0.0117 | 0.2267 | 0.3661 | 0.6075 |
| water_sealake | blur | DRA-Inspect-AC | 0.9683 | 1.0948 | 0.0267 | 0.5250 | 0.6767 | 0.7492 |
| water_sealake | jpeg | PatchCore-CF | 0.9604 | 1.4971 | 0.0633 | 0.7883 | 0.8515 | 0.8625 |
| water_sealake | jpeg | PatchCore-AC | 0.9604 | 0.9608 | 0.0783 | 0.8483 | 0.8806 | 0.8850 |
| water_sealake | jpeg | DRA-Inspect-CF | 0.9652 | 2.3174 | 0.0567 | 0.7500 | 0.8303 | 0.8467 |
| water_sealake | jpeg | DRA-Inspect-AC | 0.9652 | 1.2673 | 0.0800 | 0.9167 | 0.9182 | 0.9183 |
| water_sealake | light | PatchCore-CF | 0.9659 | 1.9988 | 0.0333 | 0.6200 | 0.7500 | 0.7933 |
| water_sealake | light | PatchCore-AC | 0.9659 | 1.2858 | 0.0517 | 0.7133 | 0.8083 | 0.8308 |
| water_sealake | light | DRA-Inspect-CF | 0.9676 | 2.0381 | 0.0350 | 0.6283 | 0.7555 | 0.7967 |
| water_sealake | light | DRA-Inspect-AC | 0.9676 | 1.1148 | 0.0717 | 0.8883 | 0.9065 | 0.9083 |
| water_sealake | lowres | PatchCore-CF | 0.9577 | 1.7603 | 0.0333 | 0.4850 | 0.6389 | 0.7258 |
| water_sealake | lowres | PatchCore-AC | 0.9577 | 1.1296 | 0.0433 | 0.6117 | 0.7392 | 0.7842 |
| water_sealake | lowres | DRA-Inspect-CF | 0.9674 | 2.1041 | 0.0100 | 0.1500 | 0.2586 | 0.5700 |
| water_sealake | lowres | DRA-Inspect-AC | 0.9674 | 1.1497 | 0.0200 | 0.3933 | 0.5566 | 0.6867 |
| water_sealake | noise | PatchCore-CF | 0.9601 | 1.0131 | 0.0433 | 0.6400 | 0.7604 | 0.7983 |
| water_sealake | noise | PatchCore-AC | 0.9601 | 0.6491 | 0.0583 | 0.7250 | 0.8131 | 0.8333 |
| water_sealake | noise | DRA-Inspect-CF | 0.9627 | 1.4211 | 0.0367 | 0.5250 | 0.6724 | 0.7442 |
| water_sealake | noise | DRA-Inspect-AC | 0.9627 | 0.7772 | 0.0650 | 0.7883 | 0.8507 | 0.8617 |

## Averaged by Setting

| Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| PatchCore-CF | 0.9582 | 1.0098 | 0.0573 | 0.7148 | 0.8004 | 0.8287 |
| PatchCore-AC | 0.9582 | 1.3401 | 0.0536 | 0.7261 | 0.8122 | 0.8363 |
| DRA-Inspect-CF | 0.9622 | 1.2134 | 0.0221 | 0.5056 | 0.6198 | 0.7417 |
| DRA-Inspect-AC | 0.9622 | 1.2735 | 0.0427 | 0.6546 | 0.7388 | 0.8059 |

