"""
Figure 11: RDMs and fits for different resolutions
"""
# other 3rd party imports
import numpy as np
import pandas as pd

# python imports
import subprocess

# module imports
from submm.constants import PATHS, PARTITIONS, PARTITION_COLORS
from submm.utils.rsm_utils import load_rsms, fit_rdm, get_lower_tri
from submm.utils.os_utils import savefig
from submm.utils.plot_utils import bar_with_err, blueblackred

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402


def build_regressors(add_intercept=True):
    """
    Provides regressor matrix for linear fits
    """
    regressor_indices = [
        np.repeat(np.arange(5), 6),  # domains
        np.repeat(np.arange(10), 3),  # categories
        np.tile(np.arange(3), 10),  # depths
    ]

    regressors = []
    for indices in regressor_indices:
        base = np.zeros((30, 30))
        xx, yy = np.meshgrid(indices, indices)
        base[xx == yy] = 1

        regressors.append(get_lower_tri(1 - base, with_diagonal=True))

    if add_intercept:
        ones_matrix = np.ones((30, 30))
        regressors.append(get_lower_tri(ones_matrix, with_diagonal=True))

    return np.array(regressors)


def plot_partition_weights(axes, partition_weights):
    """
    Produces plot showing fit betas for each partition across subjects
    """

    for (partition, weights), ax in zip(partition_weights.items(), axes):
        bar_with_err(ax, 0, weights[:, 0], mn_axis=0)
        bar_with_err(ax, 1, weights[:, 1], mn_axis=0)
        bar_with_err(ax, 2, weights[:, 2], mn_axis=0)
        bar_with_err(ax, 3, weights[:, 3], mn_axis=0)
        ax.axhline(0, c="k", linewidth=0.5)

        ax.set_xticks([0, 1, 2, 3])
        ax.set_xticklabels(
            ["Domains", "Categories", "Depths", "Intercept"], rotation=45
        )
        ax.set_ylim([-0.1, 1])

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(partition)
        ax.set_ylabel(r"$\beta$")


def plot_beta_scatter(ax, partition_weights):
    """
    Compare domain / category betas for each partition
    """
    for (partition, weights), color in zip(partition_weights.items(), PARTITION_COLORS):
        if partition == "hOc1":
            continue

        wl_mean = np.mean(weights, axis=0)
        wl_sem = np.std(weights, axis=0) / np.sqrt(weights.shape[0])

        ax.scatter(weights[:, 1], weights[:, 0], s=250, c=color, alpha=0.4)
        ax.errorbar(
            wl_mean[1],
            wl_mean[0],
            yerr=wl_sem[0],
            xerr=wl_sem[1],
            color=color,
            linewidth=6,
        )

    ax.axis("square")
    lims = ax.get_xlim()
    mx = lims[1]
    nearest_tenth = np.ceil(mx * 10) / 10.0
    ax.plot([0, mx], [0, mx], c="gray", linestyle="dashed")
    ax.set_xticks([nearest_tenth])
    ax.set_yticks([0, nearest_tenth])

    ax.set_xlim([0, mx])
    ax.set_ylim([0, ax.get_ylim()[1]])
    ax.set_xlabel(r"$\beta_{Categories}$")
    ax.set_ylabel(r"$\beta_{Domains}$")


def get_partition_weights(thresh="thr_75", glm_dir="GLM_vanilla", noise_type="none"):
    rsms = load_rsms(thresh=thresh, glm_dir=glm_dir, noise_type=noise_type)
    rdms = {partition: 1 - x for (partition, x) in rsms.items()}
    regressors = build_regressors()

    # fit domain, category, and depth weights to each rdm
    partition_weights = {}
    for partition in PARTITIONS:
        partition_rdms = rdms[partition]

        weights_list = []
        for rdm in partition_rdms:
            lower_tri_rdm = get_lower_tri(rdm, with_diagonal=True)
            weights = fit_rdm(lower_tri_rdm, regressors, method="lsq")
            weights_list.append(weights)

        partition_weights[partition] = np.stack(weights_list)

    return partition_weights, rdms


def plot_group_average_rdm(ax, rdm):
    average_rdm = np.mean(rdm, axis=0)
    ax.imshow(average_rdm, cmap=blueblackred, clim=[0.5, 1.5])
    ax.axis("off")


def make_plots(partition_weight_dict, rdm_dict):
    """
    """

    fig, axes = plt.subplots(figsize=(20, 20), nrows=3, ncols=3)

    col_keys = ["high_resolution", "low_resolution", "low_resolution_noise"]

    for col_idx, col_key in enumerate(col_keys):
        plot_group_average_rdm(axes[0, col_idx], rdm_dict[col_key]["VTC_lateral"])
        plot_group_average_rdm(axes[1, col_idx], rdm_dict[col_key]["VTC_medial"])
        plot_beta_scatter(axes[2, col_idx], partition_weight_dict[col_key])

    # add a ylabel to the leftmost plot
    for ax in axes.ravel():
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    savefig(f"{PATHS['figures']}/figure_11_rescomp.png")
    plt.close(fig)


def prepare_dataframe(partition_weight_dict):
    """
    Sets up pandas dataframe with the following fields:
        - partitions
        - subjects
        - ratios
        - R2s
    """

    partitions_list = []
    subjects_list = []
    regressors_list = []
    data_src_list = []
    values_list = []

    data_sources = partition_weight_dict.keys()

    for data_source_idx, data_source in enumerate(data_sources):
        partition_weights = partition_weight_dict[data_source]

        for partition_idx, (partition_name, weights) in enumerate(
            partition_weights.items()
        ):
            if partition_name == "hOc1":
                continue

            for regressor_idx in range(2):
                regressor_weights = weights[:, regressor_idx]

                for sub_idx in range(regressor_weights.shape[0]):

                    # IVs
                    partitions_list.append(partition_idx)
                    subjects_list.append(sub_idx)
                    regressors_list.append(regressor_idx)
                    data_src_list.append(data_source_idx)

                    # DVs
                    values_list.append(regressor_weights[sub_idx])

    partitions_list = np.array(partitions_list)
    subjects_list = np.array(subjects_list)
    regressors_list = np.array(regressors_list)
    data_src_list = np.array(data_src_list)
    values_list = np.array(values_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "regressors": regressors_list,
        "data_srcs": data_src_list,
        "values": values_list,
    }

    return pd.DataFrame(data=data)


def run_ANOVA(partition_weight_dict, key1, key2):
    hires_lowres_dict = {
        key1: partition_weight_dict[key1],
        key2: partition_weight_dict[key2],
    }
    data = prepare_dataframe(hires_lowres_dict)
    fpath = f"{PATHS['r_scripts']}/data/rescomp.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/rescomp_script.r {fpath}", shell=True
    )


def do_stats(partition_weight_dict):
    """
    Conducts two ANOVAs with
        - ROI
        - Subject
        - Data source

        as factors

        1. Data sources are hi-res and low-res
        2. Data sources are hi-res and low-res with noise
    """
    print("~~~~~~~~~~~~~~~~0.8mm vs. 2.4mm~~~~~~~~~~~~~~~")
    run_ANOVA(partition_weight_dict, "high_resolution", "low_resolution")

    print("~~~~~~~~~~~~~~~~0.8mm vs. 2.4mm+noise~~~~~~~~~~~~~~~")
    run_ANOVA(partition_weight_dict, "high_resolution", "low_resolution_noise")


def main():
    """
    Wrapper for plotting functions and statistical functions
    """
    # global plot params
    plt.rcParams.update({"font.size": 28})

    partition_weight_dict = {}
    data_sources = {
        "high_resolution": {
            "glm_dir": "GLM_vanilla",
            "thresh": "thr_75",
            "noise_type": "none",
        },
        "low_resolution": {
            "glm_dir": "GLM_vanilla_sim2pt4",
            "thresh": "thr_75",
            "noise_type": "none",
        },
        "low_resolution_noise": {
            "glm_dir": "GLM_vanilla_sim2pt4",
            "thresh": "thr_75",
            "noise_type": "gaussian",
        },
    }

    partition_weight_dict = {}
    rdm_dict = {}
    for name, params in data_sources.items():
        partition_weights, rdms = get_partition_weights(**params)
        partition_weight_dict[name] = partition_weights
        rdm_dict[name] = rdms

    # make and save plots
    make_plots(partition_weight_dict, rdm_dict)

    # do some statistics
    do_stats(partition_weight_dict)


if __name__ == "__main__":
    main()
