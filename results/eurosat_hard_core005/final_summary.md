# EuroSAT-Hard Main Summary

## Protocol-Wise Results

| Protocol | Degradation | Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | PatchCore-CF | 0.9441 | 0.4666 | 0.0550 | 0.6883 | 0.7897 | 0.8167 |
| urban_residential | blur | PatchCore-AC | 0.9441 | 1.2476 | 0.0483 | 0.6500 | 0.7655 | 0.8008 |
| urban_residential | blur | DRA-Inspect-CF | 0.9472 | 0.5258 | 0.0000 | 0.0983 | 0.1791 | 0.5492 |
| urban_residential | blur | DRA-Inspect-AC | 0.9472 | 1.0838 | 0.0017 | 0.1783 | 0.3023 | 0.5883 |
| urban_residential | jpeg | PatchCore-CF | 0.9352 | 0.4655 | 0.1167 | 0.8217 | 0.8478 | 0.8525 |
| urban_residential | jpeg | PatchCore-AC | 0.9352 | 1.2449 | 0.1000 | 0.7983 | 0.8411 | 0.8492 |
| urban_residential | jpeg | DRA-Inspect-CF | 0.9271 | 0.4834 | 0.0683 | 0.6783 | 0.7767 | 0.8050 |
| urban_residential | jpeg | DRA-Inspect-AC | 0.9271 | 0.9964 | 0.1300 | 0.8250 | 0.8440 | 0.8475 |
| urban_residential | light | PatchCore-CF | 0.9597 | 0.5299 | 0.0183 | 0.5767 | 0.7231 | 0.7792 |
| urban_residential | light | PatchCore-AC | 0.9597 | 1.4170 | 0.0167 | 0.5433 | 0.6966 | 0.7633 |
| urban_residential | light | DRA-Inspect-CF | 0.9563 | 0.5252 | 0.0150 | 0.4867 | 0.6482 | 0.7358 |
| urban_residential | light | DRA-Inspect-AC | 0.9563 | 1.0826 | 0.0367 | 0.6817 | 0.7934 | 0.8225 |
| urban_residential | lowres | PatchCore-CF | 0.9384 | 0.4531 | 0.0750 | 0.7433 | 0.8176 | 0.8342 |
| urban_residential | lowres | PatchCore-AC | 0.9384 | 1.2115 | 0.0700 | 0.7017 | 0.7921 | 0.8158 |
| urban_residential | lowres | DRA-Inspect-CF | 0.9444 | 0.5270 | 0.0000 | 0.0850 | 0.1567 | 0.5425 |
| urban_residential | lowres | DRA-Inspect-AC | 0.9444 | 1.0863 | 0.0000 | 0.1483 | 0.2583 | 0.5742 |
| urban_residential | noise | PatchCore-CF | 0.9407 | 0.4846 | 0.0333 | 0.6000 | 0.7347 | 0.7833 |
| urban_residential | noise | PatchCore-AC | 0.9407 | 1.2959 | 0.0300 | 0.5667 | 0.7098 | 0.7683 |
| urban_residential | noise | DRA-Inspect-CF | 0.9368 | 0.5086 | 0.0167 | 0.4633 | 0.6261 | 0.7233 |
| urban_residential | noise | DRA-Inspect-AC | 0.9368 | 1.0483 | 0.0417 | 0.6167 | 0.7437 | 0.7875 |
| vegetation_forest | blur | PatchCore-CF | 0.9730 | 0.9636 | 0.0600 | 0.8517 | 0.8910 | 0.8958 |
| vegetation_forest | blur | PatchCore-AC | 0.9730 | 1.7575 | 0.0400 | 0.8233 | 0.8837 | 0.8917 |
| vegetation_forest | blur | DRA-Inspect-CF | 0.9809 | 1.2234 | 0.0000 | 0.5633 | 0.7207 | 0.7817 |
| vegetation_forest | blur | DRA-Inspect-AC | 0.9809 | 1.7780 | 0.0050 | 0.6750 | 0.8036 | 0.8350 |
| vegetation_forest | jpeg | PatchCore-CF | 0.9536 | 0.8322 | 0.1600 | 0.8967 | 0.8720 | 0.8683 |
| vegetation_forest | jpeg | PatchCore-AC | 0.9536 | 1.5178 | 0.1283 | 0.8800 | 0.8763 | 0.8758 |
| vegetation_forest | jpeg | DRA-Inspect-CF | 0.9713 | 1.1386 | 0.0500 | 0.8433 | 0.8908 | 0.8967 |
| vegetation_forest | jpeg | DRA-Inspect-AC | 0.9713 | 1.6546 | 0.0900 | 0.8950 | 0.9018 | 0.9025 |
| vegetation_forest | light | PatchCore-CF | 0.9717 | 0.9839 | 0.0300 | 0.7883 | 0.8671 | 0.8792 |
| vegetation_forest | light | PatchCore-AC | 0.9717 | 1.7944 | 0.0233 | 0.7650 | 0.8555 | 0.8708 |
| vegetation_forest | light | DRA-Inspect-CF | 0.9746 | 1.0162 | 0.0283 | 0.8000 | 0.8751 | 0.8858 |
| vegetation_forest | light | DRA-Inspect-AC | 0.9746 | 1.4768 | 0.0500 | 0.8700 | 0.9062 | 0.9100 |
| vegetation_forest | lowres | PatchCore-CF | 0.9692 | 0.9407 | 0.0650 | 0.8483 | 0.8868 | 0.8917 |
| vegetation_forest | lowres | PatchCore-AC | 0.9692 | 1.7157 | 0.0483 | 0.8217 | 0.8788 | 0.8867 |
| vegetation_forest | lowres | DRA-Inspect-CF | 0.9799 | 1.2784 | 0.0000 | 0.5083 | 0.6740 | 0.7542 |
| vegetation_forest | lowres | DRA-Inspect-AC | 0.9799 | 1.8578 | 0.0017 | 0.5900 | 0.7414 | 0.7942 |
| vegetation_forest | noise | PatchCore-CF | 0.9707 | 0.9118 | 0.0200 | 0.7767 | 0.8646 | 0.8783 |
| vegetation_forest | noise | PatchCore-AC | 0.9707 | 1.6631 | 0.0133 | 0.7433 | 0.8463 | 0.8650 |
| vegetation_forest | noise | DRA-Inspect-CF | 0.9714 | 1.0704 | 0.0067 | 0.7133 | 0.8295 | 0.8533 |
| vegetation_forest | noise | DRA-Inspect-AC | 0.9714 | 1.5555 | 0.0267 | 0.8083 | 0.8810 | 0.8908 |
| water_sealake | blur | PatchCore-CF | 0.9567 | 1.8027 | 0.0350 | 0.5200 | 0.6688 | 0.7425 |
| water_sealake | blur | PatchCore-AC | 0.9567 | 1.1340 | 0.0400 | 0.6017 | 0.7330 | 0.7808 |
| water_sealake | blur | DRA-Inspect-CF | 0.9671 | 2.0139 | 0.0117 | 0.2183 | 0.3550 | 0.6033 |
| water_sealake | blur | DRA-Inspect-AC | 0.9671 | 1.1087 | 0.0333 | 0.5567 | 0.7002 | 0.7617 |
| water_sealake | jpeg | PatchCore-CF | 0.9590 | 1.5063 | 0.0600 | 0.7667 | 0.8394 | 0.8533 |
| water_sealake | jpeg | PatchCore-AC | 0.9590 | 0.9475 | 0.0767 | 0.8233 | 0.8667 | 0.8733 |
| water_sealake | jpeg | DRA-Inspect-CF | 0.9637 | 2.2947 | 0.0567 | 0.7317 | 0.8183 | 0.8375 |
| water_sealake | jpeg | DRA-Inspect-AC | 0.9637 | 1.2633 | 0.0817 | 0.9133 | 0.9156 | 0.9158 |
| water_sealake | light | PatchCore-CF | 0.9640 | 1.9930 | 0.0350 | 0.6067 | 0.7391 | 0.7858 |
| water_sealake | light | PatchCore-AC | 0.9640 | 1.2537 | 0.0450 | 0.6717 | 0.7825 | 0.8133 |
| water_sealake | light | DRA-Inspect-CF | 0.9663 | 2.0428 | 0.0317 | 0.6083 | 0.7419 | 0.7883 |
| water_sealake | light | DRA-Inspect-AC | 0.9663 | 1.1247 | 0.0700 | 0.8867 | 0.9063 | 0.9083 |
| water_sealake | lowres | PatchCore-CF | 0.9557 | 1.7726 | 0.0333 | 0.4800 | 0.6344 | 0.7233 |
| water_sealake | lowres | PatchCore-AC | 0.9557 | 1.1150 | 0.0433 | 0.5767 | 0.7119 | 0.7667 |
| water_sealake | lowres | DRA-Inspect-CF | 0.9655 | 2.1165 | 0.0100 | 0.1533 | 0.2636 | 0.5717 |
| water_sealake | lowres | DRA-Inspect-AC | 0.9655 | 1.1652 | 0.0233 | 0.4133 | 0.5754 | 0.6950 |
| water_sealake | noise | PatchCore-CF | 0.9596 | 1.0125 | 0.0467 | 0.5950 | 0.7249 | 0.7742 |
| water_sealake | noise | PatchCore-AC | 0.9596 | 0.6369 | 0.0550 | 0.6833 | 0.7862 | 0.8142 |
| water_sealake | noise | DRA-Inspect-CF | 0.9619 | 1.4236 | 0.0283 | 0.4967 | 0.6514 | 0.7342 |
| water_sealake | noise | DRA-Inspect-AC | 0.9619 | 0.7837 | 0.0567 | 0.7800 | 0.8494 | 0.8617 |

## Averaged by Setting

| Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| PatchCore-CF | 0.9568 | 1.0079 | 0.0562 | 0.7040 | 0.7934 | 0.8239 |
| PatchCore-AC | 0.9568 | 1.3302 | 0.0519 | 0.7100 | 0.8017 | 0.8291 |
| DRA-Inspect-CF | 0.9610 | 1.2126 | 0.0216 | 0.4966 | 0.6138 | 0.7375 |
| DRA-Inspect-AC | 0.9610 | 1.2711 | 0.0432 | 0.6559 | 0.7415 | 0.8063 |

