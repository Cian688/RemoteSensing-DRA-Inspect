# EuroSAT-Hard PaDiM Summary

## Protocol-Wise Results

| Protocol | Degradation | Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | PaDiM-CF | 0.9564 | 2.1388 | 0.0267 | 0.6750 | 0.7933 | 0.8242 |
| urban_residential | blur | PaDiM-AC | 0.9564 | 1.3910 | 0.0333 | 0.6900 | 0.8008 | 0.8283 |
| urban_residential | jpeg | PaDiM-CF | 0.9571 | 2.2824 | 0.0800 | 0.8333 | 0.8711 | 0.8767 |
| urban_residential | jpeg | PaDiM-AC | 0.9571 | 1.4625 | 0.0850 | 0.8383 | 0.8718 | 0.8767 |
| urban_residential | light | PaDiM-CF | 0.9691 | 2.5775 | 0.0167 | 0.6600 | 0.7873 | 0.8217 |
| urban_residential | light | PaDiM-AC | 0.9691 | 1.6563 | 0.0167 | 0.6717 | 0.7957 | 0.8275 |
| urban_residential | lowres | PaDiM-CF | 0.9519 | 2.0611 | 0.0483 | 0.7367 | 0.8254 | 0.8442 |
| urban_residential | lowres | PaDiM-AC | 0.9519 | 1.3216 | 0.0533 | 0.7483 | 0.8307 | 0.8475 |
| urban_residential | noise | PaDiM-CF | 0.9686 | 2.2182 | 0.0683 | 0.8817 | 0.9043 | 0.9067 |
| urban_residential | noise | PaDiM-AC | 0.9686 | 1.4197 | 0.0750 | 0.8850 | 0.9031 | 0.9050 |
| vegetation_forest | blur | PaDiM-CF | 0.9657 | 4.2543 | 0.0500 | 0.8033 | 0.8669 | 0.8767 |
| vegetation_forest | blur | PaDiM-AC | 0.9657 | 1.7128 | 0.0117 | 0.6667 | 0.7944 | 0.8275 |
| vegetation_forest | jpeg | PaDiM-CF | 0.9170 | 3.3540 | 0.2133 | 0.8867 | 0.8444 | 0.8367 |
| vegetation_forest | jpeg | PaDiM-AC | 0.9170 | 1.3601 | 0.1217 | 0.7800 | 0.8203 | 0.8292 |
| vegetation_forest | light | PaDiM-CF | 0.9722 | 4.3277 | 0.0217 | 0.7650 | 0.8563 | 0.8717 |
| vegetation_forest | light | PaDiM-AC | 0.9722 | 1.7563 | 0.0033 | 0.6100 | 0.7562 | 0.8033 |
| vegetation_forest | lowres | PaDiM-CF | 0.9337 | 3.7010 | 0.1167 | 0.8050 | 0.8378 | 0.8442 |
| vegetation_forest | lowres | PaDiM-AC | 0.9337 | 1.4865 | 0.0567 | 0.6650 | 0.7725 | 0.8042 |
| vegetation_forest | noise | PaDiM-CF | 0.9780 | 3.6470 | 0.0917 | 0.9350 | 0.9227 | 0.9217 |
| vegetation_forest | noise | PaDiM-AC | 0.9780 | 1.4639 | 0.0200 | 0.8183 | 0.8903 | 0.8992 |
| water_sealake | blur | PaDiM-CF | 0.9679 | 7.0103 | 0.0450 | 0.7350 | 0.8258 | 0.8450 |
| water_sealake | blur | PaDiM-AC | 0.9679 | 1.4234 | 0.0433 | 0.7100 | 0.8099 | 0.8333 |
| water_sealake | jpeg | PaDiM-CF | 0.9693 | 5.1421 | 0.0750 | 0.8900 | 0.9059 | 0.9075 |
| water_sealake | jpeg | PaDiM-AC | 0.9693 | 1.0528 | 0.0733 | 0.8800 | 0.9010 | 0.9033 |
| water_sealake | light | PaDiM-CF | 0.9735 | 7.7016 | 0.0417 | 0.7433 | 0.8329 | 0.8508 |
| water_sealake | light | PaDiM-AC | 0.9735 | 1.5638 | 0.0383 | 0.7133 | 0.8145 | 0.8375 |
| water_sealake | lowres | PaDiM-CF | 0.9676 | 6.3121 | 0.0400 | 0.6850 | 0.7942 | 0.8225 |
| water_sealake | lowres | PaDiM-AC | 0.9676 | 1.2785 | 0.0383 | 0.6567 | 0.7748 | 0.8092 |
| water_sealake | noise | PaDiM-CF | 0.9699 | 4.0303 | 0.0950 | 0.9583 | 0.9334 | 0.9317 |
| water_sealake | noise | PaDiM-AC | 0.9699 | 0.8193 | 0.0900 | 0.9483 | 0.9305 | 0.9292 |

## Averaged by Setting

| Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| PaDiM-CF | 0.9612 | 4.0506 | 0.0687 | 0.7996 | 0.8535 | 0.8654 |
| PaDiM-AC | 0.9612 | 1.4112 | 0.0507 | 0.7521 | 0.8311 | 0.8507 |

