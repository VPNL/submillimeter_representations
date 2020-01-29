"""
Figure 12: Comparison of different GLM metrics
"""

# Repo imports
import numpy as np

from submm.constants import PATHS, PARTITION_COLORS
from submm.utils.rsm_utils import load_rsms, fit_rdm, get_lower_tri
import submm.utils.plot_utils as plot_utils
from submm.utils.os_utils import mkdirquiet, savefig

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402
import matplotlib.cm  # noqa:E402


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


def get_partition_weights(rsms):
    rdms = {partition: 1 - x for (partition, x) in rsms.items()}
    regressors = build_regressors()

    # fit domain, category, and depth weights to each rdm
    partition_weights = {}
    for partition in ["VTC_lateral", "VTC_medial"]:
        partition_rdms = rdms[partition]

        weights_list = []
        for rdm in partition_rdms:
            lower_tri_rdm = get_lower_tri(rdm, with_diagonal=True)
            weights = fit_rdm(lower_tri_rdm, regressors, method="lsq")
            weights_list.append(weights)

        partition_weights[partition] = np.stack(weights_list)

    return partition_weights


def plot_beta_scatter(ax, partition_weights):
    """
    Compare domain / category betas for each partition
    """
    for (_, weights), color in zip(partition_weights.items(), PARTITION_COLORS):

        wl_mean = np.mean(weights, axis=0)
        wl_sem = np.std(weights, axis=0) / np.sqrt(weights.shape[0])

        ax.scatter(weights[:, 1], weights[:, 0], s=100, c=color, alpha=0.4)
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
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def make_plots(save_dir):
    """
    Entry point for script
    """

    rdm_plot_params = {
        "beta": {"cmap": plot_utils.blueblackred, "clim": [0, 1]},
        "tnorm": {"cmap": plot_utils.blueblackred, "clim": [0, 1]},
        "tstat": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "zscore": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "znorm": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "betasub": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
    }

    fig, axes = plt.subplots(figsize=(14, 24), nrows=6, ncols=3)

    key_order = ["znorm", "tstat", "zscore", "betasub", "tnorm", "beta"]
    for metric_idx, metric in enumerate(key_order):
        print(f"Plotting metric: {metric}")
        rsms = load_rsms(metric=metric, partitions=["VTC_lateral", "VTC_medial"])

        partition_weights = get_partition_weights(rsms)

        mean_rdms = {}
        for rsm_name, rsm in rsms.items():
            mean_rdms[rsm_name] = np.mean(1 - rsm, axis=0, keepdims=True)

        plot_utils.plot_rdms(
            axes[metric_idx, :2],
            mean_rdms,
            cmap=rdm_plot_params[metric]["cmap"],
            clim=rdm_plot_params[metric]["clim"],
        )
        plot_beta_scatter(axes[metric_idx, 2], partition_weights)

    savefig(f"{save_dir}/all_metrics.png")


def main():
    plt.rcParams.update({"font.size": 14})
    save_dir = f"{PATHS['figures']}/figure_12_metric_comparison"
    mkdirquiet(save_dir)
    make_plots(save_dir)


if __name__ == "__main__":
    main()
