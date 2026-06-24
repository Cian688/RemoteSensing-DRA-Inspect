# EuroSAT-Hard Main Summary

## Protocol-Wise Results

| Protocol | Degradation | Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| urban_residential | blur | PatchCore-CF | 0.9425 | 0.4601 | 0.0500 | 0.6433 | 0.7598 | 0.7967 |
| urban_residential | blur | PatchCore-AC | 0.9425 | 1.2150 | 0.0500 | 0.6483 | 0.7635 | 0.7992 |
| urban_residential | blur | DRA-Inspect-CF | 0.9448 | 0.5215 | 0.0000 | 0.1250 | 0.2222 | 0.5625 |
| urban_residential | blur | DRA-Inspect-AC | 0.9448 | 1.0866 | 0.0033 | 0.1983 | 0.3301 | 0.5975 |
| urban_residential | jpeg | PatchCore-CF | 0.9354 | 0.4641 | 0.1000 | 0.7900 | 0.8360 | 0.8450 |
| urban_residential | jpeg | PatchCore-AC | 0.9354 | 1.2256 | 0.1000 | 0.7950 | 0.8391 | 0.8475 |
| urban_residential | jpeg | DRA-Inspect-CF | 0.9274 | 0.4822 | 0.0700 | 0.6883 | 0.7829 | 0.8092 |
| urban_residential | jpeg | DRA-Inspect-AC | 0.9274 | 1.0046 | 0.1283 | 0.8217 | 0.8427 | 0.8467 |
| urban_residential | light | PatchCore-CF | 0.9575 | 0.5307 | 0.0167 | 0.5433 | 0.6966 | 0.7633 |
| urban_residential | light | PatchCore-AC | 0.9575 | 1.4015 | 0.0167 | 0.5483 | 0.7007 | 0.7658 |
| urban_residential | light | DRA-Inspect-CF | 0.9545 | 0.5229 | 0.0133 | 0.4917 | 0.6534 | 0.7392 |
| urban_residential | light | DRA-Inspect-AC | 0.9545 | 1.0895 | 0.0350 | 0.6633 | 0.7812 | 0.8142 |
| urban_residential | lowres | PatchCore-CF | 0.9355 | 0.4443 | 0.0633 | 0.6733 | 0.7754 | 0.8050 |
| urban_residential | lowres | PatchCore-AC | 0.9355 | 1.1731 | 0.0633 | 0.6850 | 0.7836 | 0.8108 |
| urban_residential | lowres | DRA-Inspect-CF | 0.9426 | 0.5226 | 0.0000 | 0.0983 | 0.1791 | 0.5492 |
| urban_residential | lowres | DRA-Inspect-AC | 0.9426 | 1.0887 | 0.0000 | 0.1717 | 0.2930 | 0.5858 |
| urban_residential | noise | PatchCore-CF | 0.9391 | 0.4835 | 0.0300 | 0.5633 | 0.7071 | 0.7667 |
| urban_residential | noise | PatchCore-AC | 0.9391 | 1.2768 | 0.0300 | 0.5683 | 0.7112 | 0.7692 |
| urban_residential | noise | DRA-Inspect-CF | 0.9341 | 0.5046 | 0.0183 | 0.4717 | 0.6331 | 0.7267 |
| urban_residential | noise | DRA-Inspect-AC | 0.9341 | 1.0512 | 0.0433 | 0.6133 | 0.7404 | 0.7850 |
| vegetation_forest | blur | PatchCore-CF | 0.9685 | 0.9549 | 0.0667 | 0.8367 | 0.8792 | 0.8850 |
| vegetation_forest | blur | PatchCore-AC | 0.9685 | 1.6872 | 0.0433 | 0.8083 | 0.8731 | 0.8825 |
| vegetation_forest | blur | DRA-Inspect-CF | 0.9782 | 1.2162 | 0.0000 | 0.5533 | 0.7124 | 0.7767 |
| vegetation_forest | blur | DRA-Inspect-AC | 0.9782 | 1.7465 | 0.0067 | 0.6667 | 0.7968 | 0.8300 |
| vegetation_forest | jpeg | PatchCore-CF | 0.9466 | 0.8145 | 0.1617 | 0.8867 | 0.8657 | 0.8625 |
| vegetation_forest | jpeg | PatchCore-AC | 0.9466 | 1.4391 | 0.1233 | 0.8583 | 0.8663 | 0.8675 |
| vegetation_forest | jpeg | DRA-Inspect-CF | 0.9693 | 1.1137 | 0.0350 | 0.8200 | 0.8841 | 0.8925 |
| vegetation_forest | jpeg | DRA-Inspect-AC | 0.9693 | 1.5993 | 0.0850 | 0.8833 | 0.8975 | 0.8992 |
| vegetation_forest | light | PatchCore-CF | 0.9665 | 0.9578 | 0.0300 | 0.7750 | 0.8587 | 0.8725 |
| vegetation_forest | light | PatchCore-AC | 0.9665 | 1.6924 | 0.0233 | 0.7317 | 0.8338 | 0.8542 |
| vegetation_forest | light | DRA-Inspect-CF | 0.9699 | 0.9960 | 0.0267 | 0.7683 | 0.8561 | 0.8708 |
| vegetation_forest | light | DRA-Inspect-AC | 0.9699 | 1.4303 | 0.0483 | 0.8600 | 0.9013 | 0.9058 |
| vegetation_forest | lowres | PatchCore-CF | 0.9627 | 0.9130 | 0.0717 | 0.8367 | 0.8769 | 0.8825 |
| vegetation_forest | lowres | PatchCore-AC | 0.9627 | 1.6133 | 0.0467 | 0.8000 | 0.8664 | 0.8767 |
| vegetation_forest | lowres | DRA-Inspect-CF | 0.9766 | 1.2642 | 0.0000 | 0.5017 | 0.6681 | 0.7508 |
| vegetation_forest | lowres | DRA-Inspect-AC | 0.9766 | 1.8154 | 0.0033 | 0.5883 | 0.7393 | 0.7925 |
| vegetation_forest | noise | PatchCore-CF | 0.9685 | 0.9052 | 0.0183 | 0.7617 | 0.8558 | 0.8717 |
| vegetation_forest | noise | PatchCore-AC | 0.9685 | 1.5995 | 0.0133 | 0.7117 | 0.8251 | 0.8492 |
| vegetation_forest | noise | DRA-Inspect-CF | 0.9698 | 1.0635 | 0.0033 | 0.6783 | 0.8067 | 0.8375 |
| vegetation_forest | noise | DRA-Inspect-AC | 0.9698 | 1.5273 | 0.0250 | 0.7817 | 0.8653 | 0.8783 |
| water_sealake | blur | PatchCore-CF | 0.9525 | 1.7730 | 0.0400 | 0.5067 | 0.6552 | 0.7333 |
| water_sealake | blur | PatchCore-AC | 0.9525 | 1.1287 | 0.0550 | 0.6200 | 0.7403 | 0.7825 |
| water_sealake | blur | DRA-Inspect-CF | 0.9642 | 2.0345 | 0.0133 | 0.2583 | 0.4063 | 0.6225 |
| water_sealake | blur | DRA-Inspect-AC | 0.9642 | 1.1156 | 0.0267 | 0.5333 | 0.6838 | 0.7533 |
| water_sealake | jpeg | PatchCore-CF | 0.9557 | 1.4885 | 0.0633 | 0.7433 | 0.8229 | 0.8400 |
| water_sealake | jpeg | PatchCore-AC | 0.9557 | 0.9476 | 0.0767 | 0.8200 | 0.8647 | 0.8717 |
| water_sealake | jpeg | DRA-Inspect-CF | 0.9612 | 2.2266 | 0.0517 | 0.7100 | 0.8061 | 0.8292 |
| water_sealake | jpeg | DRA-Inspect-AC | 0.9612 | 1.2209 | 0.0800 | 0.8817 | 0.8989 | 0.9008 |
| water_sealake | light | PatchCore-CF | 0.9593 | 1.9754 | 0.0400 | 0.5833 | 0.7187 | 0.7717 |
| water_sealake | light | PatchCore-AC | 0.9593 | 1.2576 | 0.0517 | 0.6717 | 0.7795 | 0.8100 |
| water_sealake | light | DRA-Inspect-CF | 0.9629 | 2.0367 | 0.0367 | 0.6033 | 0.7358 | 0.7833 |
| water_sealake | light | DRA-Inspect-AC | 0.9629 | 1.1168 | 0.0683 | 0.8300 | 0.8745 | 0.8808 |
| water_sealake | lowres | PatchCore-CF | 0.9521 | 1.7216 | 0.0367 | 0.4583 | 0.6132 | 0.7108 |
| water_sealake | lowres | PatchCore-AC | 0.9521 | 1.0960 | 0.0517 | 0.5683 | 0.7016 | 0.7583 |
| water_sealake | lowres | DRA-Inspect-CF | 0.9626 | 2.1380 | 0.0100 | 0.1933 | 0.3213 | 0.5917 |
| water_sealake | lowres | DRA-Inspect-AC | 0.9626 | 1.1723 | 0.0217 | 0.3983 | 0.5610 | 0.6883 |
| water_sealake | noise | PatchCore-CF | 0.9566 | 1.0282 | 0.0417 | 0.5467 | 0.6884 | 0.7525 |
| water_sealake | noise | PatchCore-AC | 0.9566 | 0.6546 | 0.0533 | 0.6467 | 0.7608 | 0.7967 |
| water_sealake | noise | DRA-Inspect-CF | 0.9599 | 1.4211 | 0.0300 | 0.4650 | 0.6221 | 0.7175 |
| water_sealake | noise | DRA-Inspect-AC | 0.9599 | 0.7792 | 0.0517 | 0.7100 | 0.8061 | 0.8292 |

## Averaged by Setting

| Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| PatchCore-CF | 0.9533 | 0.9943 | 0.0553 | 0.6766 | 0.7740 | 0.8106 |
| PatchCore-AC | 0.9533 | 1.2939 | 0.0532 | 0.6988 | 0.7940 | 0.8228 |
| DRA-Inspect-CF | 0.9585 | 1.2043 | 0.0206 | 0.4951 | 0.6193 | 0.7373 |
| DRA-Inspect-AC | 0.9585 | 1.2563 | 0.0418 | 0.6401 | 0.7341 | 0.7992 |

