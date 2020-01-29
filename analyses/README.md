## Analyses
The scripts here describe how the relevants outputs, e.g., RDMs, are computed from GLM outputs or raw timeseries. In addition to the scripts in `utils/`, these scripts assume that [Kendrick Kay's `knkutils`](https://github.com/kendrickkay/knkutils) have been added to the path.

### Table of Contents
1. [GLM](#glm)
1. [ROIs](#rois)
1. [tSNR](#tsnr)
1. [Parse GLMs](#parseglms)
1. [Maps](#maps)
1. [Metric Means](#metric-means)
1. [EPI Maps](#epi-maps)
1. [RDMs](#rdms)
1. [R^2 Control Analysis](#r2-control)

### GLMs [00]<a name="glm"></a>
Running `analyses/00_run_glms/main.m` runs three GLMs for each participant:
	1. One with odd runs only
	2. One with even runs only
	3. One with all runs
Additionally, the GLM is run for both high-resolution and simulated low-resolution data.

### ROIs [01]<a name="rois"></a>
The scripts in this directory are used to either draw ROIs in each participant or to transform the hOc1 (V1) ROI into each subjects' native space.

### tSNR [02]<a name="tsnr"></a>
Running `analyses/02_tsnr/main.m` does the following:
Computes the mean tSNR at each cortical depth, averaged across the entire ROI.

### Parse GLMs [03]<a name="parseglms"></a>
Running `analyses/03_parse_glms/main.m` extracts values at each vertex based on ROI, vein masking, and other restrictions. It also computes the GLM metrics specified in `analyses/Constants.m` for each vertex, and saves everything to a big .mat file.

### Maps [04] <a name="maps"></a>
`analyses/04_maps/main.m` saves maps of GLM metrics in each VTC ROI for each subject and each depth


### Mean EPI Maps [04a] <a name="epi-maps"></a>
`analyses/04a_epi_mask_redoutline/main.m` plots in a red outline the 'dark' vertices that we identify as likely veins and exclude from most analyses.

### Metric Means [05] <a name="metric-means"></a>
`analyses/04_maps/main.m` saves maps of GLM metrics in each VTC ROI for each subject and each depth

### RSMs [06] <a name="rsms"></a>
`analyses/06_rsms/main.m` is a function used to save RSMs across depths and conditions. 
`analyses/06_rsms/main_r2_control.m` is identical, but further restricts vertices based on the results from `07_variance_explained/`, i.e., sets of vertices matched for variance explained across partitions

### R2 matching [07]<a name="r2-control"></a>
`analyses/05_r2_matching` has a few scripts:
1. `write_matching_indices.m`: finds and writes the indices for vertices in each partition that are matched for R2
2. `analyze_mean_vals.m`: performs statistical tests that population at each is matched in R2
3. `main.m`: saves R2 in each partition after doing matching for later statistical testing across, e.g., depths
