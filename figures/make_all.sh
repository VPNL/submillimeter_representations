#!/bin/sh

PATH_TO_VIRTUALENV="/Users/eshed/submmtest"
source ${PATH_TO_VIRTUALENV}/bin/activate

# runs all figure scripts back to back
echo "--------------------Figure 1A: Stimuli..."
python figure_1a_stimuli.py

echo "--------------------Figure 3AC: 3T znorm maps..."
python figure_3ac_3t_znorm_maps.py

echo "--------------------Figure 3B: 3T RDM comparison"
python figure_3b_rdm_comparison.py

echo "--------------------Figure 4A: 7T znorm maps..."
python figure_4a_znorm_maps.py

echo "--------------------Figure 4B: 7T znorm maps across depth..."
python figure_4b_znorm_maps_both_hemis.py

echo "--------------------Figure 5: hypothetical RSMs and embeddings..."
python figure_5_hypothetical_rdms_embeddings.py

echo "--------------------Figure 6: group averaged RDMs and MDS embeddings..."
python figure_6_group_average_rdms.py

echo "--------------------Figure 6: group averaged RDMs and MDS embeddings (simulated 2.4mm)..."
python figure_6_group_average_rdms.py --glm_dir GLM_vanilla_sim2pt4

echo "--------------------Figure 7A: rdm fit diagram..."
python figure_7a_rdm_fit_diagram.py

echo "--------------------Figure 7B: rdm fits..."
python figure_7b_rdm_fits.py

echo "--------------------Figure 7B: rdm fits (simulated 2.4mm)..."
python figure_7b_rdm_fits.py --glm_dir GLM_vanilla_sim2pt4

echo "--------------------Figure 7B: rdm fits (simulated 2.4mm with noise)..."
python figure_7b_rdm_fits.py --glm_dir GLM_vanilla_sim2pt4 --noise_type gaussian

echo "--------------------Figure 7B: rdm fits (R-squared control)..."
python figure_7b_rdm_fits.py --r2_control

echo "--------------------Figure 7B: rdm fits (thresh_0)..."
python figure_7b_rdm_fits.py --thresh thr_0

echo "--------------------Figure 8: Group-averaged RDMs by depth..."
python figure_8af_average_rdms_by_depth.py

echo "--------------------Figure 8GH: RDM fits by depth..."
python figure_8gh_rdm_fits_by_depth.py

echo "--------------------Figure 8GH: RDM fits by depth (simulated 2.4mm)..."
python figure_8gh_rdm_fits_by_depth.py --glm_dir GLM_vanilla_sim2pt4

echo "--------------------Figure 8GH: RDM fits by depth (simulated 2.4mm with noise)..."
python figure_8gh_rdm_fits_by_depth.py --glm_dir GLM_vanilla_sim2pt4 --noise_type gaussian

echo "--------------------Figure 8GH: RDM fits by depth (R-squared control)..."
python figure_8gh_rdm_fits_by_depth.py --r2_control

echo "--------------------Figure 8GH: RDM fits by depth (thresh_0)..."
python figure_8gh_rdm_fits_by_depth.py --thresh thr_0

echo "--------------------Figure 9: rdm fits by domain..."
python figure_9_rdm_fits_by_domain.py

echo "--------------------Figure 10A, 10B: tSNR and R2..."
python figure_10ab_tsnr_R2.py

echo "--------------------Figure 10C: Metric means..."
python figure_10c_metric_means.py

echo "--------------------Figure 11: Resolution comparison for fits..."
python figure_11_rescomp.py

echo "--------------------Figure 12: Metric comparison..."
python figure_12_metric_comparison.py

