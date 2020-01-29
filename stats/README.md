# `stats/`

## Statistical results produced elsewhere
1. Many of the statistics that relate to figures are produced alongside figures to avoid code duplication
1. One script in analyses, `analyses/07_variance_explained/analyze_mean_vals.m` does the statistics for R2 matching instead of saving all of the values to `outputs/`.

## Directory of scripts (alphabetical)

#### `abs_rdm_rescomp.py` 
Compares mean absolute RDM magnitude across resolutions (0.8mm/2.4mm).

```bash
python abs_rsm_rescomp.py [--use_noisy_lowres]
```

Use the `--use_noisy_lowres` flag if comparing 0.8mm to the 2.4mm+noise dataset.

#### `interroi_rdm_correlation.py` 
Evaluates correlation of lower triangles of RDMs between partitions, e.g., lateral VTC vs. V1, medial VTC vs V1

```bash
python intersubject_rsm_correlations.py
```

#### `intersubject_rdm_correlation.py` 
Evaluates similarity of RSMs in each partition across participants

```bash
python intersubject_rsm_correlations.py
```

#### `C1051_3t_7t_rdm_corr.py` 
Evaluates similarity between C1051's 3T and 7T 2.4mm data

```bash
python kk_3t_7t_rsm_corr.py
```

#### `split_half_rel.py` 
Computes split half reliability for 30x30 RDMs

```bash
python split_half_rel.py
```
