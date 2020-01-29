"""
Figure 10C: mean betas across categories and depths
"""
import subprocess
import argparse

# Repo imports
import numpy as np
import pandas as pd
import h5py
from submm.constants import (
    PATHS,
    FSID_SESSIONS,
    CONTRASTS,
    CATEGORY_COLORS,
    METRICS,
    PARTITIONS,
)
from submm.utils.stats import sem
from submm.utils.os_utils import mkdirquiet, savefig

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402


def load_means(
    metric="tstat", partition="VTC_lateral", abs_string="noabs", r2_control=False
):
    """
    Retrieve metric means for the specified metric
    """

    data = np.zeros((len(FSID_SESSIONS), len(CONTRASTS), 3))

    mm_path = PATHS["metric_means_r2control"] if r2_control else PATHS["metric_means"]
    with h5py.File(mm_path, "r") as f:
        for i, FSID_SESSION in enumerate(FSID_SESSIONS):
            for j, contrast in enumerate(CONTRASTS):
                data[i, j, :] = f["means"][FSID_SESSION]["GLM_vanilla"][metric][
                    partition
                ][contrast][abs_string][:].squeeze()

    return data


def plot_means(ax, means, metric=""):
    bar_width = 0.2
    # FSID x category x depth
    for category_idx, color in enumerate(CATEGORY_COLORS):
        category_data = means[:, category_idx, :].squeeze()
        subject_mean = np.mean(category_data, axis=0)
        subject_sem = sem(category_data, axis=0)
        ax.bar(
            category_idx - 0.2,
            subject_mean[0],
            yerr=subject_sem[0],
            width=bar_width,
            facecolor=color,
        )
        ax.bar(
            category_idx,
            subject_mean[1],
            yerr=subject_sem[1],
            width=bar_width,
            facecolor=color,
        )
        ax.bar(
            category_idx + 0.2,
            subject_mean[2],
            yerr=subject_sem[2],
            width=bar_width,
            facecolor=color,
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.set_xticks([])
        ax.axhline(0, color="k")


def prepare_dataframe(lateral_betas, medial_betas):
    """
    Prepares pandas dataframe that can be easily saved to R for ANOVA
    """

    partitions_list = []
    category_list = []
    depth_list = []
    subjects_list = []

    betas_list = []

    for partition_idx, partition_betas in enumerate([lateral_betas, medial_betas]):

        for category_idx in range(partition_betas.shape[1]):
            category_betas = partition_betas[:, category_idx, :]

            for depth_idx in range(3):
                depth_betas = category_betas[:, depth_idx]

                for sub_idx, depth_beta in enumerate(depth_betas):
                    # IVs
                    partitions_list.append(partition_idx)
                    category_list.append(category_idx)
                    depth_list.append(depth_idx - 1)
                    subjects_list.append(sub_idx)

                    # DV
                    betas_list.append(depth_beta)

    partitions_list = np.array(partitions_list)
    category_list = np.array(category_list)
    depth_list = np.array(depth_list)
    subjects_list = np.array(subjects_list)
    betas_list = np.array(betas_list)

    data = {
        "partitions": partitions_list,
        "categories": category_list,
        "depths": depth_list,
        "subjects": subjects_list,
        "betas": betas_list,
    }

    return pd.DataFrame(data=data)


def main():
    """
    Entry point for script
    """

    font = {"size": 18}
    matplotlib.rc("font", **font)
    save_dir = f"{PATHS['figures']}/figure_10c_metric_means"
    mkdirquiet(save_dir)

    # do stats for betas only
    lateral_betas = load_means(
        metric="beta",
        partition="VTC_lateral",
        abs_string="noabs",
        r2_control=ARGS.r2_control,
    )
    medial_betas = load_means(
        metric="beta",
        partition="VTC_medial",
        abs_string="noabs",
        r2_control=ARGS.r2_control,
    )

    data = prepare_dataframe(lateral_betas, medial_betas)
    fpath = f"{PATHS['r_scripts']}/data/raw_betas.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/raw_betas_script.r {fpath}", shell=True
    )

    for abs_string in ["abs", "noabs"]:
        for metric in METRICS + ["beta"]:
            print(f"Plotting metric: {metric}")
            fig, axes = plt.subplots(figsize=(16, 4), ncols=3, sharey=True)

            for ax, partition in zip(axes, PARTITIONS):
                partition_means = load_means(
                    metric=metric, partition=partition, abs_string=abs_string
                )

                plot_means(ax, partition_means, metric=metric)

            savefig(f"{save_dir}/{metric}_{abs_string}.png")
            plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--r2_control", action="store_true")
    ARGS, _ = parser.parse_known_args()
    main()
