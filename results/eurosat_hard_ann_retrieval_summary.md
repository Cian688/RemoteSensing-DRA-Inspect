# EuroSAT-Hard Approximate Retrieval Summary

Approximate retrieval uses an IVF-style coarse-to-fine search on the same saved DRA memory bank, with recalibrated q50/q95 statistics under the approximate backend.

- Approx. settings: nlist=256, nprobe=4, train_samples=20000, kmeans_iters=6, max_candidates=8192

| Ratio | Retrieval | AUROC | FPR | TPR | F1 | BAcc | ms/img | Speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.10 | Exact | 0.9622 | 0.0427 | 0.6554 | 0.7395 | 0.8064 | 505.43 | 1.00x |
| 0.10 | Approx. IVF | 0.9249 | 0.0416 | 0.4671 | 0.5918 | 0.7128 | 37.40 | 13.52x |
| 0.02 | Exact | 0.9593 | 0.0426 | 0.6363 | 0.7285 | 0.7969 | 97.78 | 1.00x |
| 0.02 | Approx. IVF | 0.9362 | 0.0399 | 0.4920 | 0.6084 | 0.7261 | 35.48 | 2.76x |

