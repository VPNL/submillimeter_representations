"""
Figure 10A and 10B: tSNR and R-squared plots, respectively
"""

# other 3rd party imports
import subprocess
import h5py
import numpy as np
import pandas as pd
import scipy.stats as stats

# Repo imports
from submm.constants import PATHS
from submm.utils.plot_utils import bar_with_err
from submm.utils.os_utils import savefig

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402


def load_tsnr(partition="VTC_lateral"):
    """
    Loads tSNR data from .mat file for the specified partition

    Returns
        tsnr (3, 7): depths x subjects matrix of tSNR values averaged
            across the partition specified

    NB
        This is computed on stone and transferred over, not computed
            over vertices here. See analyses/02_tsnr .
    """

    data_path = f"{PATHS['tsnr']}"
    with h5py.File(data_path, "r") as f:
        tsnr = f["tsnr_struct"][partition][:]

    return tsnr


def load_R2(partition="VTC_lateral"):
    """
    Loads r_squared data from .mat file for the specified partition
    Averages odd and even values!

    Returns
        R2 (3, 7): depths x subjects matrix of tSNR values averaged
            across the partition specified

    """

    data_path = f"{PATHS['r2']}"
    with h5py.File(data_path, "r") as f:
        odd_r2 = f["r2_struct"]["odd"][partition][:] / 100.0  # convert back to fraction
        even_r2 = f["r2_struct"]["even"][partition][:] / 100.0
        stacked_r2 = np.stack((odd_r2, even_r2))[
            :, :, :7
        ]  # remove the 8th subject (3T data) if it exists
        r2 = np.mean(stacked_r2, axis=0)

    return r2


def plot_vals(
    ax, lateral, medial, ylabel="tSNR", xticklabels=None, width=0.35, group_gap=0.05
):
    """
    Plots the provided values as bar graphs with error bars
    Inputs:
        {lateral, medial}: 3 x n_subjects
        ylabel (str)
        width: how wide each bar should be
        group_gap: how much space should be left between groups
    """

    xs = np.arange(3)
    offsets = width / 2.0 + group_gap / 2.0
    bar_with_err(ax, xs - offsets, lateral, width=width, color="k")
    bar_with_err(ax, xs + offsets, medial, width=width, color="gray")

    ax.set_xticks(np.arange(0, 3))

    ax.set_xticklabels(["Superficial", "Middle", "Deep"])
    ax.set_ylabel(ylabel)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def report_range(lateral, medial, metric="tSNR"):
    """
    Prints min and max across partitions and depths
    """
    lateral_mn = np.mean(lateral, axis=1)
    medial_mn = np.mean(medial, axis=1)
    all_mn = np.hstack((lateral_mn, medial_mn))
    print(f"{metric} ranges from {np.min(all_mn):.2f} to {np.max(all_mn):.2f}")


def prepare_dataframe(lateral_values, medial_values):
    """
    Inputs
        {lateral,medial}_values: 3x7 (depths x participants) matrices for
            the given metric
    """
    partitions_list = []
    subjects_list = []
    depths_list = []
    values_list = []

    for partition_idx, partition_values in enumerate([lateral_values, medial_values]):
        for depth_idx in range(3):
            depth_values = partition_values[depth_idx, :]

            for sub_idx in range(depth_values.shape[0]):
                # IVs
                partitions_list.append(partition_idx)
                subjects_list.append(sub_idx)
                depths_list.append(
                    depth_idx - 1
                )  # subtract 1 to center the depth values to -1, 0, 1

                # DV
                values_list.append(depth_values[sub_idx])

    partitions_list = np.array(partitions_list)
    subjects_list = np.array(subjects_list)
    depths_list = np.array(depths_list)
    values_list = np.array(values_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "depths": depths_list,
        "values": values_list,
    }

    return pd.DataFrame(data=data)


def main():
    """
    Entry point for script
    """
    font = {"size": 18}
    matplotlib.rc("font", **font)

    # create dictionary specifying data and plot options
    metrics = {
        "tSNR": {
            "lateral": load_tsnr(partition="VTC_lateral"),
            "medial": load_tsnr(partition="VTC_medial"),
            "ylabel": "tSNR",
        },
        "R2": {
            "lateral": load_R2(partition="VTC_lateral"),
            "medial": load_R2(partition="VTC_medial"),
            "ylabel": r"$R^2$",
        },
    }

    # make plots
    fig, axes = plt.subplots(figsize=(12, 4), ncols=2, gridspec_kw={"wspace": 0.4})

    for (metric_name, metric_vals), ax in zip(metrics.items(), axes):
        print(f"==============={metric_name}================")
        lateral = metric_vals["lateral"]
        medial = metric_vals["medial"]

        plot_vals(ax, lateral, medial, ylabel=metric_vals["ylabel"])
        report_range(lateral, medial, metric=metric_name)

        data = prepare_dataframe(lateral, medial)

        # call the R script
        fpath = f"{PATHS['r_scripts']}/data/metrics_by_depth.csv"
        data.to_csv(fpath)
        subprocess.call(
            f"Rscript --vanilla {PATHS['r_scripts']}/metrics_by_depth_script.r {fpath}",
            shell=True,
        )

    savefig(f"{PATHS['figures']}/figure_10ab_tsnr_r2.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
