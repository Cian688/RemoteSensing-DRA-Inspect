# NWPU-RESISC45 Hard Extended Summary

## Protocol-Wise Results

| Protocol | Degradation | Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| infrastructure_airport | blur | PatchCore-CF | 0.7908 | 0.3089 | 0.0143 | 0.3262 | 0.4868 | 0.6560 |
| infrastructure_airport | blur | PatchCore-AC | 0.7908 | 0.8360 | 0.0429 | 0.3901 | 0.5446 | 0.6736 |
| infrastructure_airport | blur | DRA-Inspect-CF | 0.8138 | 0.3347 | 0.0000 | 0.2411 | 0.3886 | 0.6206 |
| infrastructure_airport | blur | DRA-Inspect-AC | 0.8138 | 0.8418 | 0.0000 | 0.3121 | 0.4757 | 0.6560 |
| infrastructure_airport | jpeg | PatchCore-CF | 0.8004 | 0.3509 | 0.0429 | 0.4610 | 0.6132 | 0.7091 |
| infrastructure_airport | jpeg | PatchCore-AC | 0.8004 | 0.9495 | 0.0929 | 0.5532 | 0.6724 | 0.7302 |
| infrastructure_airport | jpeg | DRA-Inspect-CF | 0.7986 | 0.3533 | 0.0500 | 0.5319 | 0.6726 | 0.7410 |
| infrastructure_airport | jpeg | DRA-Inspect-AC | 0.7986 | 0.8888 | 0.0786 | 0.5532 | 0.6783 | 0.7373 |
| infrastructure_airport | light | PatchCore-CF | 0.8055 | 0.3148 | 0.0071 | 0.2482 | 0.3955 | 0.6205 |
| infrastructure_airport | light | PatchCore-AC | 0.8055 | 0.8520 | 0.0071 | 0.3262 | 0.4894 | 0.6595 |
| infrastructure_airport | light | DRA-Inspect-CF | 0.8080 | 0.3202 | 0.0000 | 0.2624 | 0.4157 | 0.6312 |
| infrastructure_airport | light | DRA-Inspect-AC | 0.8080 | 0.8055 | 0.0071 | 0.3262 | 0.4894 | 0.6595 |
| infrastructure_airport | lowres | PatchCore-CF | 0.7868 | 0.2922 | 0.0071 | 0.3404 | 0.5053 | 0.6666 |
| infrastructure_airport | lowres | PatchCore-AC | 0.7868 | 0.7907 | 0.0357 | 0.4113 | 0.5686 | 0.6878 |
| infrastructure_airport | lowres | DRA-Inspect-CF | 0.8152 | 0.3253 | 0.0000 | 0.2482 | 0.3977 | 0.6241 |
| infrastructure_airport | lowres | DRA-Inspect-AC | 0.8152 | 0.8182 | 0.0071 | 0.2979 | 0.4565 | 0.6454 |
| infrastructure_airport | noise | PatchCore-CF | 0.7995 | 0.3469 | 0.0357 | 0.3830 | 0.5400 | 0.6736 |
| infrastructure_airport | noise | PatchCore-AC | 0.7995 | 0.9389 | 0.0643 | 0.5177 | 0.6547 | 0.7267 |
| infrastructure_airport | noise | DRA-Inspect-CF | 0.8033 | 0.3537 | 0.0429 | 0.4255 | 0.5797 | 0.6913 |
| infrastructure_airport | noise | DRA-Inspect-AC | 0.8033 | 0.8897 | 0.0643 | 0.5106 | 0.6486 | 0.7232 |
| urban_dense | blur | PatchCore-CF | 0.7770 | 0.2376 | 0.0143 | 0.1571 | 0.2683 | 0.5714 |
| urban_dense | blur | PatchCore-AC | 0.7770 | 0.5594 | 0.0214 | 0.2000 | 0.3275 | 0.5893 |
| urban_dense | blur | DRA-Inspect-CF | 0.7805 | 0.2434 | 0.0000 | 0.0714 | 0.1333 | 0.5357 |
| urban_dense | blur | DRA-Inspect-AC | 0.7805 | 0.5550 | 0.0143 | 0.1357 | 0.2360 | 0.5607 |
| urban_dense | jpeg | PatchCore-CF | 0.7547 | 0.2343 | 0.0286 | 0.2214 | 0.3543 | 0.5964 |
| urban_dense | jpeg | PatchCore-AC | 0.7547 | 0.5515 | 0.0643 | 0.3071 | 0.4479 | 0.6214 |
| urban_dense | jpeg | DRA-Inspect-CF | 0.7472 | 0.2259 | 0.0286 | 0.2357 | 0.3729 | 0.6036 |
| urban_dense | jpeg | DRA-Inspect-AC | 0.7472 | 0.5151 | 0.0857 | 0.3571 | 0.4950 | 0.6357 |
| urban_dense | light | PatchCore-CF | 0.7853 | 0.2471 | 0.0071 | 0.0714 | 0.1325 | 0.5321 |
| urban_dense | light | PatchCore-AC | 0.7853 | 0.5817 | 0.0214 | 0.1286 | 0.2236 | 0.5536 |
| urban_dense | light | DRA-Inspect-CF | 0.7784 | 0.2388 | 0.0000 | 0.0714 | 0.1333 | 0.5357 |
| urban_dense | light | DRA-Inspect-AC | 0.7784 | 0.5447 | 0.0214 | 0.1429 | 0.2454 | 0.5607 |
| urban_dense | lowres | PatchCore-CF | 0.7676 | 0.2227 | 0.0143 | 0.1286 | 0.2250 | 0.5571 |
| urban_dense | lowres | PatchCore-AC | 0.7676 | 0.5241 | 0.0357 | 0.2000 | 0.3237 | 0.5821 |
| urban_dense | lowres | DRA-Inspect-CF | 0.7743 | 0.2332 | 0.0071 | 0.0714 | 0.1325 | 0.5321 |
| urban_dense | lowres | DRA-Inspect-AC | 0.7743 | 0.5318 | 0.0143 | 0.1286 | 0.2250 | 0.5571 |
| urban_dense | noise | PatchCore-CF | 0.7741 | 0.2458 | 0.0214 | 0.1786 | 0.2976 | 0.5786 |
| urban_dense | noise | PatchCore-AC | 0.7741 | 0.5787 | 0.0429 | 0.2214 | 0.3503 | 0.5893 |
| urban_dense | noise | DRA-Inspect-CF | 0.7693 | 0.2391 | 0.0214 | 0.1643 | 0.2771 | 0.5714 |
| urban_dense | noise | DRA-Inspect-AC | 0.7693 | 0.5452 | 0.0429 | 0.2429 | 0.3778 | 0.6000 |
| vegetation_forest | blur | PatchCore-CF | 0.6719 | 0.2325 | 0.0357 | 0.1571 | 0.2635 | 0.5607 |
| vegetation_forest | blur | PatchCore-AC | 0.6719 | 0.3031 | 0.0429 | 0.2214 | 0.3503 | 0.5893 |
| vegetation_forest | blur | DRA-Inspect-CF | 0.6956 | 0.2721 | 0.0286 | 0.1071 | 0.1887 | 0.5393 |
| vegetation_forest | blur | DRA-Inspect-AC | 0.6956 | 0.3454 | 0.0357 | 0.1786 | 0.2941 | 0.5714 |
| vegetation_forest | jpeg | PatchCore-CF | 0.6817 | 0.3034 | 0.0429 | 0.2571 | 0.3956 | 0.6071 |
| vegetation_forest | jpeg | PatchCore-AC | 0.6817 | 0.3955 | 0.0500 | 0.2929 | 0.4362 | 0.6214 |
| vegetation_forest | jpeg | DRA-Inspect-CF | 0.6934 | 0.3161 | 0.0429 | 0.2429 | 0.3778 | 0.6000 |
| vegetation_forest | jpeg | DRA-Inspect-AC | 0.6934 | 0.4013 | 0.0571 | 0.3357 | 0.4821 | 0.6393 |
| vegetation_forest | light | PatchCore-CF | 0.7051 | 0.3199 | 0.0429 | 0.1071 | 0.1863 | 0.5321 |
| vegetation_forest | light | PatchCore-AC | 0.7051 | 0.4170 | 0.0429 | 0.1571 | 0.2619 | 0.5571 |
| vegetation_forest | light | DRA-Inspect-CF | 0.7164 | 0.3371 | 0.0429 | 0.0929 | 0.1635 | 0.5250 |
| vegetation_forest | light | DRA-Inspect-AC | 0.7164 | 0.4279 | 0.0500 | 0.1857 | 0.3006 | 0.5679 |
| vegetation_forest | lowres | PatchCore-CF | 0.6676 | 0.2218 | 0.0357 | 0.1714 | 0.2840 | 0.5679 |
| vegetation_forest | lowres | PatchCore-AC | 0.6676 | 0.2891 | 0.0429 | 0.2214 | 0.3503 | 0.5893 |
| vegetation_forest | lowres | DRA-Inspect-CF | 0.6913 | 0.2594 | 0.0286 | 0.1143 | 0.2000 | 0.5429 |
| vegetation_forest | lowres | DRA-Inspect-AC | 0.6913 | 0.3293 | 0.0357 | 0.1786 | 0.2941 | 0.5714 |
| vegetation_forest | noise | PatchCore-CF | 0.6860 | 0.3084 | 0.0429 | 0.1643 | 0.2722 | 0.5607 |
| vegetation_forest | noise | PatchCore-AC | 0.6860 | 0.4020 | 0.0500 | 0.1857 | 0.3006 | 0.5679 |
| vegetation_forest | noise | DRA-Inspect-CF | 0.6928 | 0.3215 | 0.0500 | 0.1500 | 0.2500 | 0.5500 |
| vegetation_forest | noise | DRA-Inspect-AC | 0.6928 | 0.4081 | 0.0500 | 0.2357 | 0.3667 | 0.5929 |

## Averaged by Setting

| Method | AUROC | Gap | Fixed FPR | Fixed TPR | Fixed F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| PatchCore-CF | 0.7503 | 0.2791 | 0.0262 | 0.2249 | 0.3480 | 0.5993 |
| PatchCore-AC | 0.7503 | 0.5980 | 0.0438 | 0.2890 | 0.4201 | 0.6226 |
| DRA-Inspect-CF | 0.7585 | 0.2916 | 0.0229 | 0.2020 | 0.3122 | 0.5896 |
| DRA-Inspect-AC | 0.7585 | 0.5899 | 0.0376 | 0.2748 | 0.4044 | 0.6186 |

