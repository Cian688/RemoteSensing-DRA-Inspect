# NWPU-RESISC45 Hard Extended Appendix Tables

## Protocol-Wise

| Protocol | Method | AUROC | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| infrastructure_airport | PatchCore-AC | 0.7966 | 0.0486 | 0.4397 | 0.5859 | 0.6956 |
| infrastructure_airport | DRA-Inspect-AC | 0.8078 | 0.0314 | 0.4000 | 0.5497 | 0.6843 |
| infrastructure_airport | DRA-Inspect-AC (matched FPR) |  | 0.0443 | 0.4312 | 0.5761 | 0.6935 |
| urban_dense | PatchCore-AC | 0.7718 | 0.0371 | 0.2114 | 0.3346 | 0.5871 |
| urban_dense | DRA-Inspect-AC | 0.7699 | 0.0357 | 0.2014 | 0.3159 | 0.5829 |
| urban_dense | DRA-Inspect-AC (matched FPR) |  | 0.0371 | 0.2329 | 0.3567 | 0.5979 |
| vegetation_forest | PatchCore-AC | 0.6824 | 0.0457 | 0.2157 | 0.3398 | 0.5850 |
| vegetation_forest | DRA-Inspect-AC | 0.6979 | 0.0457 | 0.2229 | 0.3475 | 0.5886 |
| vegetation_forest | DRA-Inspect-AC (matched FPR) |  | 0.0500 | 0.2571 | 0.3884 | 0.6036 |

## Degradation-Wise

| Degradation | Method | AUROC | FPR | TPR | F1 | BAcc |
| --- | --- | --- | --- | --- | --- | --- |
| noise | PatchCore-AC | 0.7532 | 0.0524 | 0.3083 | 0.4352 | 0.6280 |
| noise | DRA-Inspect-AC | 0.7551 | 0.0524 | 0.3297 | 0.4644 | 0.6387 |
| blur | PatchCore-AC | 0.7466 | 0.0357 | 0.2705 | 0.4074 | 0.6174 |
| blur | DRA-Inspect-AC | 0.7633 | 0.0167 | 0.2088 | 0.3353 | 0.5961 |
| light | PatchCore-AC | 0.7653 | 0.0238 | 0.2040 | 0.3250 | 0.5901 |
| light | DRA-Inspect-AC | 0.7676 | 0.0262 | 0.2183 | 0.3451 | 0.5960 |
| lowres | PatchCore-AC | 0.7407 | 0.0381 | 0.2776 | 0.4142 | 0.6197 |
| lowres | DRA-Inspect-AC | 0.7603 | 0.0190 | 0.2017 | 0.3252 | 0.5913 |
| jpeg | PatchCore-AC | 0.7456 | 0.0690 | 0.3844 | 0.5188 | 0.6577 |
| jpeg | DRA-Inspect-AC | 0.7464 | 0.0738 | 0.4153 | 0.5518 | 0.6708 |

