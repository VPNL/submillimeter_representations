"""
Compute and compare absolute RDM magnitude at 0.8mm and 2.4mm
"""

import argparse
import subprocess

import numpy as np
import pandas as pd

from submm.constants import PATHS
from submm.utils.rsm_utils import load_rsms, get_lower_tri
from submm.utils.stats import report_ttest_2_sample


def prepare_dataframe(hires_rdms, lowres_rdms):
    """
    Sets up pandas dataframe with the following fields:
        - partitions
        - subjects
        - data_srcs (resolutions)
        - magnitudes
    """

    data_src_list = list()
    subjects_list = list()
    partitions_list = list()
    magnitudes_list = list()

    for data_src_idx, rdms in enumerate([hires_rdms, lowres_rdms]):

        for partition_idx, partition_name in enumerate(["VTC_lateral", "VTC_medial"]):

            # extract mean of lower triangle of partition RDM, keeping diagonal
            # because values are strictly positive, no need to take absolute value here
            partition_rdms = rdms[partition_name]
            lower_triangle_means = np.array(
                [np.mean(get_lower_tri(x, with_diagonal=True)) for x in partition_rdms]
            )

            for sub_idx, val in enumerate(lower_triangle_means):
                magnitudes_list.append(val)
                data_src_list.append(data_src_idx)
                subjects_list.append(sub_idx)
                partitions_list.append(partition_idx)

    subjects_list = np.array(subjects_list)
    data_src_list = np.array(data_src_list)
    partitions_list = np.array(partitions_list)
    magnitudes_list = np.array(magnitudes_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "data_srcs": data_src_list,
        "magnitudes": magnitudes_list,
    }

    return pd.DataFrame(data=data)


def main():
    """
    Entry point for analysis
    """

    noise_type = "gaussian" if ARGS.use_noisy_lowres else "none"

    # load both RSM types and covert to RDMs
    hires_rsms = load_rsms(glm_dir="GLM_vanilla")
    lowres_rsms = load_rsms(glm_dir="GLM_vanilla_sim2pt4", noise_type=noise_type)

    hires_rdms = {partition: 1 - x for (partition, x) in hires_rsms.items()}
    lowres_rdms = {partition: 1 - x for (partition, x) in lowres_rsms.items()}

    # get pandas dataframe
    data = prepare_dataframe(hires_rdms, lowres_rdms)

    # report on mean per data source
    hires_data = data[data.data_srcs == 0]
    lowres_data = data[data.data_srcs == 1]

    print("Hires RDM Magnitude vs. Lowres")
    report_ttest_2_sample(
        hires_data.magnitudes, lowres_data.magnitudes, print_mean_var=True
    )

    # run analysis of variance
    fpath = f"{PATHS['r_scripts']}/data/mean_abs_rdm.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/mean_abs_rdm_script.r {fpath}",
        shell=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use_noisy_lowres", dest="use_noisy_lowres", action="store_true"
    )
    ARGS, _ = parser.parse_known_args()
    main()
