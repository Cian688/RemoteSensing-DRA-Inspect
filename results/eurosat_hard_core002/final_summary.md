# EuroSAT-Hard Main Summary

## Protocol-Wise Results

| Protocol | Degradation | Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | PatchCore-CF | 0.9425 | 0.4678 | 0.0500 | 0.6400 | 0.7574 | 0.7950 |
| urban_residential | blur | PatchCore-AC | 0.9425 | 1.2244 | 0.0500 | 0.6450 | 0.7611 | 0.7975 |
| urban_residential | blur | DRA-Inspect-CF | 0.9447 | 0.5223 | 0.0000 | 0.1083 | 0.1955 | 0.5542 |
| urban_residential | blur | DRA-Inspect-AC | 0.9447 | 1.0752 | 0.0033 | 0.1833 | 0.3090 | 0.5900 |
| urban_residential | jpeg | PatchCore-CF | 0.9330 | 0.4661 | 0.1100 | 0.7950 | 0.8346 | 0.8425 |
| urban_residential | jpeg | PatchCore-AC | 0.9330 | 1.2199 | 0.1100 | 0.7950 | 0.8346 | 0.8425 |
| urban_residential | jpeg | DRA-Inspect-CF | 0.9279 | 0.4857 | 0.0650 | 0.6867 | 0.7840 | 0.8108 |
| urban_residential | jpeg | DRA-Inspect-AC | 0.9279 | 0.9999 | 0.1250 | 0.8083 | 0.8362 | 0.8417 |
| urban_residential | light | PatchCore-CF | 0.9578 | 0.5265 | 0.0183 | 0.5383 | 0.6916 | 0.7600 |
| urban_residential | light | PatchCore-AC | 0.9578 | 1.3782 | 0.0183 | 0.5433 | 0.6958 | 0.7625 |
| urban_residential | light | DRA-Inspect-CF | 0.9534 | 0.5214 | 0.0133 | 0.4767 | 0.6398 | 0.7317 |
| urban_residential | light | DRA-Inspect-AC | 0.9534 | 1.0734 | 0.0367 | 0.6550 | 0.7744 | 0.8092 |
| urban_residential | lowres | PatchCore-CF | 0.9369 | 0.4539 | 0.0600 | 0.6917 | 0.7897 | 0.8158 |
| urban_residential | lowres | PatchCore-AC | 0.9369 | 1.1881 | 0.0600 | 0.6950 | 0.7920 | 0.8175 |
| urban_residential | lowres | DRA-Inspect-CF | 0.9447 | 0.5283 | 0.0000 | 0.0967 | 0.1763 | 0.5483 |
| urban_residential | lowres | DRA-Inspect-AC | 0.9447 | 1.0876 | 0.0000 | 0.1500 | 0.2609 | 0.5750 |
| urban_residential | noise | PatchCore-CF | 0.9399 | 0.4867 | 0.0317 | 0.5617 | 0.7050 | 0.7650 |
| urban_residential | noise | PatchCore-AC | 0.9399 | 1.2738 | 0.0317 | 0.5633 | 0.7064 | 0.7658 |
| urban_residential | noise | DRA-Inspect-CF | 0.9349 | 0.5085 | 0.0183 | 0.4583 | 0.6208 | 0.7200 |
| urban_residential | noise | DRA-Inspect-AC | 0.9349 | 1.0469 | 0.0367 | 0.6033 | 0.7358 | 0.7833 |
| vegetation_forest | blur | PatchCore-CF | 0.9713 | 0.9731 | 0.0633 | 0.8483 | 0.8875 | 0.8925 |
| vegetation_forest | blur | PatchCore-AC | 0.9713 | 1.7662 | 0.0500 | 0.8300 | 0.8830 | 0.8900 |
| vegetation_forest | blur | DRA-Inspect-CF | 0.9793 | 1.2193 | 0.0000 | 0.5667 | 0.7234 | 0.7833 |
| vegetation_forest | blur | DRA-Inspect-AC | 0.9793 | 1.7665 | 0.0050 | 0.6700 | 0.8000 | 0.8325 |
| vegetation_forest | jpeg | PatchCore-CF | 0.9561 | 0.8412 | 0.1417 | 0.8917 | 0.8770 | 0.8750 |
| vegetation_forest | jpeg | PatchCore-AC | 0.9561 | 1.5269 | 0.1167 | 0.8750 | 0.8787 | 0.8792 |
| vegetation_forest | jpeg | DRA-Inspect-CF | 0.9696 | 1.1219 | 0.0483 | 0.8383 | 0.8887 | 0.8950 |
| vegetation_forest | jpeg | DRA-Inspect-AC | 0.9696 | 1.6254 | 0.0900 | 0.8867 | 0.8971 | 0.8983 |
| vegetation_forest | light | PatchCore-CF | 0.9696 | 0.9734 | 0.0317 | 0.7900 | 0.8673 | 0.8792 |
| vegetation_forest | light | PatchCore-AC | 0.9696 | 1.7668 | 0.0217 | 0.7550 | 0.8499 | 0.8667 |
| vegetation_forest | light | DRA-Inspect-CF | 0.9720 | 0.9995 | 0.0300 | 0.7850 | 0.8650 | 0.8775 |
| vegetation_forest | light | DRA-Inspect-AC | 0.9720 | 1.4481 | 0.0550 | 0.8633 | 0.9001 | 0.9042 |
| vegetation_forest | lowres | PatchCore-CF | 0.9682 | 0.9606 | 0.0667 | 0.8517 | 0.8879 | 0.8925 |
| vegetation_forest | lowres | PatchCore-AC | 0.9682 | 1.7436 | 0.0517 | 0.8250 | 0.8792 | 0.8867 |
| vegetation_forest | lowres | DRA-Inspect-CF | 0.9777 | 1.2716 | 0.0000 | 0.5133 | 0.6784 | 0.7567 |
| vegetation_forest | lowres | DRA-Inspect-AC | 0.9777 | 1.8422 | 0.0033 | 0.5917 | 0.7419 | 0.7942 |
| vegetation_forest | noise | PatchCore-CF | 0.9700 | 0.9099 | 0.0183 | 0.7683 | 0.8601 | 0.8750 |
| vegetation_forest | noise | PatchCore-AC | 0.9700 | 1.6516 | 0.0133 | 0.7483 | 0.8496 | 0.8675 |
| vegetation_forest | noise | DRA-Inspect-CF | 0.9700 | 1.0643 | 0.0067 | 0.7050 | 0.8238 | 0.8492 |
| vegetation_forest | noise | DRA-Inspect-AC | 0.9700 | 1.5420 | 0.0267 | 0.7883 | 0.8687 | 0.8808 |
| water_sealake | blur | PatchCore-CF | 0.9537 | 1.7760 | 0.0367 | 0.4750 | 0.6284 | 0.7192 |
| water_sealake | blur | PatchCore-AC | 0.9537 | 1.1234 | 0.0483 | 0.5917 | 0.7215 | 0.7717 |
| water_sealake | blur | DRA-Inspect-CF | 0.9643 | 2.0246 | 0.0150 | 0.2333 | 0.3738 | 0.6092 |
| water_sealake | blur | DRA-Inspect-AC | 0.9643 | 1.1089 | 0.0283 | 0.5133 | 0.6659 | 0.7425 |
| water_sealake | jpeg | PatchCore-CF | 0.9570 | 1.4851 | 0.0567 | 0.7283 | 0.8161 | 0.8358 |
| water_sealake | jpeg | PatchCore-AC | 0.9570 | 0.9394 | 0.0750 | 0.8150 | 0.8624 | 0.8700 |
| water_sealake | jpeg | DRA-Inspect-CF | 0.9625 | 2.2546 | 0.0517 | 0.6833 | 0.7877 | 0.8158 |
| water_sealake | jpeg | DRA-Inspect-AC | 0.9625 | 1.2349 | 0.0800 | 0.8917 | 0.9045 | 0.9058 |
| water_sealake | light | PatchCore-CF | 0.9607 | 1.9832 | 0.0383 | 0.5583 | 0.6994 | 0.7600 |
| water_sealake | light | PatchCore-AC | 0.9607 | 1.2545 | 0.0450 | 0.6683 | 0.7802 | 0.8117 |
| water_sealake | light | DRA-Inspect-CF | 0.9644 | 2.0381 | 0.0317 | 0.5733 | 0.7144 | 0.7708 |
| water_sealake | light | DRA-Inspect-AC | 0.9644 | 1.1163 | 0.0683 | 0.8500 | 0.8862 | 0.8908 |
| water_sealake | lowres | PatchCore-CF | 0.9535 | 1.7267 | 0.0317 | 0.4483 | 0.6059 | 0.7083 |
| water_sealake | lowres | PatchCore-AC | 0.9535 | 1.0923 | 0.0467 | 0.5583 | 0.6957 | 0.7558 |
| water_sealake | lowres | DRA-Inspect-CF | 0.9630 | 2.1258 | 0.0100 | 0.1667 | 0.2833 | 0.5783 |
| water_sealake | lowres | DRA-Inspect-AC | 0.9630 | 1.1643 | 0.0233 | 0.3833 | 0.5450 | 0.6800 |
| water_sealake | noise | PatchCore-CF | 0.9579 | 1.0177 | 0.0417 | 0.5600 | 0.6993 | 0.7592 |
| water_sealake | noise | PatchCore-AC | 0.9579 | 0.6438 | 0.0500 | 0.6550 | 0.7683 | 0.8025 |
| water_sealake | noise | DRA-Inspect-CF | 0.9607 | 1.4164 | 0.0267 | 0.4450 | 0.6048 | 0.7092 |
| water_sealake | noise | DRA-Inspect-AC | 0.9607 | 0.7758 | 0.0567 | 0.7067 | 0.8015 | 0.8250 |

## Averaged by Setting

| Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| PatchCore-CF | 0.9552 | 1.0032 | 0.0531 | 0.6764 | 0.7738 | 0.8117 |
| PatchCore-AC | 0.9552 | 1.3195 | 0.0526 | 0.7042 | 0.7972 | 0.8258 |
| DRA-Inspect-CF | 0.9593 | 1.2068 | 0.0211 | 0.4891 | 0.6106 | 0.7340 |
| DRA-Inspect-AC | 0.9593 | 1.2605 | 0.0426 | 0.6363 | 0.7285 | 0.7969 |

