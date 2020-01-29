"""
Figure 7B: Fitting RDMs from model RDMs
"""
# other 3rd party imports
import numpy as np
import pandas as pd
from tabulate import tabulate  # noqa:E401

# python imports
import argparse
import subprocess

# module imports
from submm.constants import PATHS, PARTITIONS, PARTITION_COLORS, PRIMARY_METRIC
from submm.utils.rsm_utils import load_rsms, fit_rdm, get_lower_tri
from submm.utils.stats import sem
from submm.utils.os_utils import mkdirquiet, savefig
from submm.utils.plot_utils import bar_with_err

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
        bar_with_err(
            ax,
            0,
            weights[:, 0],
            mn_axis=0,
            facecolor="k",
            ebar_kwargs={"color": "k", "linewidth": 5},
        )
        bar_with_err(
            ax,
            1,
            weights[:, 1],
            mn_axis=0,
            facecolor="none",
            edgecolor="k",
            ebar_kwargs={"color": "k", "linewidth": 5},
        )
        bar_with_err(
            ax,
            2,
            weights[:, 2],
            mn_axis=0,
            facecolor="#CCCCCC",
            ebar_kwargs={"color": "#CCCCCC", "linewidth": 5},
        )
        bar_with_err(
            ax,
            3,
            weights[:, 3],
            mn_axis=0,
            facecolor="gray",
            ebar_kwargs={"color": "gray", "linewidth": 5},
        )
        ax.axhline(0, c="k", linewidth=0.5)

        ax.set_xticks([0, 1, 2, 3])
        ax.set_xticklabels(["", "", "", ""], rotation=0)
        ax.set_ylim([-0.1, 1])

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel(r"$\beta$")


def plot_beta_scatter(ax, partition_weights):
    """
    Compare domain / category betas for each partition
    """
    for (_, weights), color in zip(partition_weights.items(), PARTITION_COLORS):

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
    ax.set_xticks(np.arange(0.1, nearest_tenth, step=0.1))
    ax.set_yticks(np.arange(0, nearest_tenth, step=0.1))
    ax.set_xlabel(r"$\beta_{Categories}$")
    ax.set_ylabel(r"$\beta_{Domains}$")
    ax.set_xlim([0, mx])
    ax.set_ylim([0, ax.get_ylim()[1]])


def get_partition_weights(
    thresh="thr_75",
    glm_dir="GLM_vanilla",
    metric=PRIMARY_METRIC,
    r2_control=False,
    noise_type="none",
):
    rsms = load_rsms(
        thresh=thresh,
        glm_dir=glm_dir,
        r2_control=r2_control,
        metric=metric,
        noise_type=noise_type,
    )
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

    return partition_weights


def make_plots(partition_weights, save_dir):
    """
    """

    # first figure: betas for each predictor
    plt.rcParams.update({"font.size": 36})
    fig, axes = plt.subplots(figsize=(21, 7), ncols=3, sharey=True)
    plot_partition_weights(axes, partition_weights)

    savefig(f"{save_dir}/fit_weights.png")
    plt.close(fig)

    # second figure: betas for each predictor
    fig, ax = plt.subplots(figsize=(10, 10), ncols=1)
    plot_beta_scatter(ax, partition_weights)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    savefig(f"{save_dir}/partition_comparison.png")
    plt.close(fig)


def prepare_dataframe(partition_weights, regressor_indices=None, roi_indices=None):
    """
    Sets up pandas dataframe with the following fields:
        - partitions
        - subjects
        - regressors
        - weights

    Inputs
        partition_weights (dict): keys are partiion names, values are number of subjects
            x regressor
        regressor_indices (list): which regressors to use, e.g., [0, 1] means only the first two
            (domain and category)
        roi_indices (list): which rois to use. Note: right now this only works because dicts are
            implicitly ordered in Python 3. Should be made more robust...

    """

    if regressor_indices is None:
        regressor_indices = np.arange(4)

    if roi_indices is None:
        roi_indices = np.arange(3)

    partitions_list = []
    subjects_list = []
    regressors_list = []

    weights_list = []

    for partition_idx, (_, weights) in enumerate(partition_weights.items()):
        if partition_idx not in roi_indices:
            continue
        for regressor_idx in regressor_indices:
            regressor_weights = weights[:, regressor_idx]

            for sub_idx in range(regressor_weights.shape[0]):
                # IVs
                partitions_list.append(partition_idx)
                subjects_list.append(sub_idx)
                regressors_list.append(regressor_idx)

                # DV
                weights_list.append(regressor_weights[sub_idx])

    partitions_list = np.array(partitions_list)
    subjects_list = np.array(subjects_list)
    regressors_list = np.array(regressors_list)
    weights_list = np.array(weights_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "regressors": regressors_list,
        "weights": weights_list,
    }

    return pd.DataFrame(data=data)


def print_partition_weight_table(partition_weights):
    """
    Prints mean and standard error the mean for each ROI and each regressor
    """
    # prepare data for tabulate
    table_rows = []
    for partition_name, weights in partition_weights.items():
        mean_across_subjects = np.mean(weights, axis=0)
        sem_across_subjects = sem(weights, axis=0)

        row = [partition_name]
        headers = ["ROI", "Domain", "Category", "Depth", "Intercept"]
        for mn, se in zip(mean_across_subjects, sem_across_subjects):
            row.append(
                f"{mn:.5f} \u00B1 {se:.5f}"
            )  # u00B1 is the unicode symbol for +/-

        table_rows.append(row)

    table = tabulate(table_rows, headers=headers, tablefmt="github")
    print(table)


def decorated_box(description=""):
    print(
        f"""
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        -----------------------------
        *****************************
        {description}
        *****************************
        -----------------------------
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
    )


def do_stats(partition_weights):
    # make table of weights by partition (for Kalanit)
    print_partition_weight_table(partition_weights)

    # ANOVA 1: Raw weights
    decorated_box(description="Domain, Category, Depth: All ROIs")
    data = prepare_dataframe(partition_weights, regressor_indices=[0, 1, 2])
    # call the R script
    fpath = f"{PATHS['r_scripts']}/data/rdm_fit_weights.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/rdm_fit_weights_script.r {fpath}",
        shell=True,
    )

    # ANOVA 2: Raw weights (domain and category only)
    decorated_box(description="Domain, Category only: All ROIs")
    data = prepare_dataframe(partition_weights, regressor_indices=[0, 1])
    # call the R script
    fpath = f"{PATHS['r_scripts']}/data/rdm_fit_weights.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/rdm_fit_weights_script.r {fpath}",
        shell=True,
    )

    # ANOVA 3: Raw weights, lateral and medial only, domain and category only
    decorated_box(description="Domain, Category: VTC_lateral and VTC_medial")
    data = prepare_dataframe(
        partition_weights, regressor_indices=[0, 1], roi_indices=[0, 1]
    )
    # call the R script
    fpath = f"{PATHS['r_scripts']}/data/rdm_fit_weights.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/rdm_fit_weights_script.r {fpath}",
        shell=True,
    )


def main():
    """
    Wrapper for plotting functions and statistical functions
    """
    # global plot params
    plt.rcParams.update({"font.size": 34})
    r2_control_str = "_r2_control" if ARGS.r2_control else ""
    noise_str = ARGS.noise_type if ARGS.noise_type != "none" else ""
    metric_str = "" if ARGS.metric == PRIMARY_METRIC else ARGS.metric
    save_dir = (
        f"{PATHS['figures']}/figure_7b_rdm_fits_"
        f"{ARGS.glm_dir}{noise_str}_{ARGS.thresh}{r2_control_str}{metric_str}"
    )
    mkdirquiet(save_dir)

    # do the RDM fits and get weights and variance explained for each RDM in
    # each partition
    args_kv_pairs = vars(ARGS)
    partition_weights = get_partition_weights(**args_kv_pairs)

    # make and save plots
    make_plots(partition_weights, save_dir)

    # do statistical analyses
    do_stats(partition_weights)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--glm_dir", type=str, help="GLM type to use", default="GLM_vanilla"
    )
    parser.add_argument(
        "--noise_type", type=str, help="one of 'gaussian' or 'none'", default="none"
    )
    parser.add_argument(
        "--thresh", type=str, help="bias_mask_threshold to use", default="thr_75"
    )
    parser.add_argument(
        "--metric", type=str, help="metric to get RDMs for", default=PRIMARY_METRIC
    )
    parser.add_argument("--r2_control", action="store_true")
    ARGS, _ = parser.parse_known_args()
    main()
