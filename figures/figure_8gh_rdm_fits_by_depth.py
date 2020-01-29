"""
Figure 9gh: Fitting RDMs from model RDMs but only with lower triangles
"""
# other 3rd party imports
import numpy as np
import pandas as pd

# python imports
import argparse
import subprocess

# module imports
from submm.constants import PATHS, PARTITION_COLORS, PARTITION_NAMES, PARTITIONS
from submm.utils.rsm_utils import load_rsms, fit_rdm, get_lower_tri, split_by_depth
from submm.utils.stats import sem, report_ttest_2_sample, report_ttest_1_sample
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
        np.repeat(np.arange(5), 2),  # domains
        np.arange(10),  # categories
    ]

    regressors = []
    for indices in regressor_indices:
        base = np.zeros((10, 10))
        xx, yy = np.meshgrid(indices, indices)
        base[xx == yy] = 1

        regressors.append(get_lower_tri(1 - base, with_diagonal=True))

    if add_intercept:
        ones_matrix = np.ones((10, 10))
        regressors.append(get_lower_tri(ones_matrix, with_diagonal=True))

    return np.array(regressors)


def plot_partition_weights(axes, partition_weights):
    """
    Produces plot showing fit betas for each partition across subjects
    """

    xticks = [0.5, 3.5, 6.5]
    xticklabels = ["Superficial", "Middle", "Deep"]
    depth_starts = [0, 3, 6]

    for partition_idx, (partition, weights) in enumerate(partition_weights.items()):
        if partition == "hOc1":
            continue
        ax = axes[partition_idx]
        partition_color = PARTITION_COLORS[partition_idx]
        for regressor in range(2):
            if regressor == 1:
                facecolor = "None"
                edgecolor = partition_color
                linewidth = 5
            else:
                facecolor = partition_color
                edgecolor = None
                linewidth = 0

            for depth in range(3):
                bar_with_err(
                    ax,
                    depth_starts[depth] + regressor,
                    weights[:, depth, regressor],
                    mn_axis=0,
                    facecolor=facecolor,
                    edgecolor=edgecolor,
                    linewidth=linewidth,
                    ebar_kwargs={"color": partition_color, "linewidth": 5},
                )

        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(PARTITION_NAMES[partition_idx])
        ax.set_ylabel(r"$\beta$")

    """
    scale y-axes to fit all the data points across partitions (since we're sharing
    the y-axis across subplots)
    """
    stacked_partition_weights = np.stack([v for (k, v) in partition_weights.items()])
    mx = max([np.max(stacked_partition_weights[:, :, :, :2]), 0.4])
    ax.set_yticks(np.arange(0, mx, step=0.1))
    for ax in axes.ravel():
        ax.set_ylim([0, mx])


def plot_beta_scatter(ax, partition_weights):
    """
    Compare domain / category betas for each partition
    """
    markers = ["^", "s", "v"]

    for (partition, weights), color in zip(partition_weights.items(), PARTITION_COLORS):
        for depth in range(3):
            depth_weights = weights[:, depth, :]

            wl_mean = np.mean(depth_weights, axis=0)
            wl_sem = sem(depth_weights, axis=0)

            # scatterplot for this depth
            ax.scatter(
                depth_weights[:, 1],
                depth_weights[:, 0],
                s=160,
                c=color,
                alpha=0.5,
                marker=markers[depth],
                edgecolor="k",
            )

            # error on each axis for this depth
            ax.errorbar(
                wl_mean[1],
                wl_mean[0],
                yerr=wl_sem[0],
                xerr=wl_sem[1],
                color=color,
                linewidth=8,
            )

            # draw small white marker at center
            ax.scatter(
                wl_mean[1],
                wl_mean[0],
                c="white",
                marker=markers[depth],
                linewidth=3,
                edgecolor=color,
                s=300,
                zorder=999999,
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


def get_partition_weights(
    thresh="thr_75", glm_dir="GLM_vanilla", r2_control=False, noise_type="none"
):
    rsms = load_rsms(
        thresh=thresh, glm_dir=glm_dir, r2_control=r2_control, noise_type=noise_type
    )
    rdms_by_depth = {
        partition: np.array([1 - split_by_depth(rsm) for rsm in partition_rsms])
        for (partition, partition_rsms) in rsms.items()
    }
    regressors = build_regressors()

    partition_weights = {}
    for partition in PARTITIONS:
        partition_rdms = rdms_by_depth[partition]
        subject_weights = []
        for subject_rdms in partition_rdms:
            depth_weights = []
            for depth_rdm in subject_rdms:
                weights = fit_rdm(
                    get_lower_tri(depth_rdm, with_diagonal=True),
                    regressors,
                    method="lsq",
                )
                depth_weights.append(weights)
            subject_weights.append(np.stack(depth_weights))
        partition_weights[partition] = np.stack(subject_weights)

    return partition_weights


def make_plots(partition_weights, save_dir):
    """
    """

    # first figure: betas for each predictor
    fig, axes = plt.subplots(figsize=(14, 7), ncols=2, sharey=True)
    plot_partition_weights(axes, partition_weights)

    savefig(f"{save_dir}/fit_weights.png")
    plt.close(fig)

    # second figure: betas for each predictor
    fig, ax = plt.subplots(figsize=(10, 10))
    plot_beta_scatter(ax, partition_weights)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    savefig(f"{save_dir}/partition_comparison.png")
    plt.close(fig)


def prepare_dataframe_betas(partition_weights):
    """
    Sets up pandas dataframe with the following fields:
        - partitions
        - subjects
        - regressors
        - depths
        - betas

    But skip intercepts.
    """

    partitions_list = []
    subjects_list = []
    depths_list = []
    regressors_list = []
    betas_list = []

    for partition_idx, (partition_name, weights) in enumerate(
        partition_weights.items()
    ):
        if partition_name == "hOc1":
            continue
        for regressor_idx in range(2):
            regressor_weights = weights[:, :, regressor_idx]

            for depth_idx in range(3):
                depth_weights = regressor_weights[:, depth_idx]

                for sub_idx in range(depth_weights.shape[0]):
                    partitions_list.append(partition_idx)
                    subjects_list.append(sub_idx)
                    depths_list.append(
                        depth_idx - 1
                    )  # subtract 1 to center the depth values to -1, 0, 1
                    betas_list.append(depth_weights[sub_idx])
                    regressors_list.append(regressor_idx)

    partitions_list = np.array(partitions_list)
    subjects_list = np.array(subjects_list)
    betas_list = np.array(betas_list)
    depths_list = np.array(depths_list)
    regressors_list = np.array(regressors_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "betas": betas_list,
        "depths": depths_list,
        "regressors": regressors_list,
    }

    return pd.DataFrame(data=data)


def prepare_dataframe_slopes(partition_weights):
    """
    Sets up pandas dataframe with the following fields:
        - partitions
        - subjects
        - slopes
        - R2s

    But skip intercepts.
    """

    partitions_list = []
    subjects_list = []
    slopes_list = []
    regressors_list = []

    for partition_idx, (partition_name, weights) in enumerate(
        partition_weights.items()
    ):
        if partition_name == "hOc1":
            continue
        for regressor_idx in range(2):
            regressor_weights = weights[:, :, regressor_idx]

            slopes = np.array(
                [
                    np.polyfit(np.arange(3), subject_weights, 1)[0]
                    for subject_weights in regressor_weights
                ]
            )

            for sub_idx in range(slopes.shape[0]):
                partitions_list.append(partition_idx)
                subjects_list.append(sub_idx)
                slopes_list.append(slopes[sub_idx])
                regressors_list.append(regressor_idx)

    partitions_list = np.array(partitions_list)
    subjects_list = np.array(subjects_list)
    slopes_list = np.array(slopes_list)
    regressors_list = np.array(regressors_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "slopes": slopes_list,
        "regressors": regressors_list,
    }

    return pd.DataFrame(data=data)


def prepare_dataframe_diffs(partition_weights):
    """
    Sets up pandas dataframe with the following fields:
        - partitions
        - subjects
        - diffs

    But skip intercepts.
    """

    partitions_list = []
    subjects_list = []
    diff_slopes_list = []

    for partition_idx, (partition_name, weights) in enumerate(
        partition_weights.items()
    ):
        diffs = weights[:, :, 0] - weights[:, :, 1]
        slopes = np.array(
            [np.polyfit(np.arange(3), subject_diffs, 1)[0] for subject_diffs in diffs]
        )

        for sub_idx in range(slopes.shape[0]):
            partitions_list.append(partition_idx)
            subjects_list.append(sub_idx)
            diff_slopes_list.append(slopes[sub_idx])

    partitions_list = np.array(partitions_list)
    subjects_list = np.array(subjects_list)
    diff_slopes_list = np.array(diff_slopes_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "diffs": diff_slopes_list,
    }

    return pd.DataFrame(data=data)


def do_stats_slopes(partition_weights):
    data = prepare_dataframe_slopes(partition_weights)

    # carry out all pairwise t-tests
    lateral_data = data[data.partitions == 0]
    medial_data = data[data.partitions == 1]

    lateral_domain_data = lateral_data[lateral_data.regressors == 0]
    medial_domain_data = medial_data[medial_data.regressors == 0]

    lateral_category_data = lateral_data[lateral_data.regressors == 1]
    medial_category_data = medial_data[medial_data.regressors == 1]

    # normal t-tests
    print("Lateral slope vs. Medial slope")
    report_ttest_2_sample(lateral_data.slopes, medial_data.slopes)

    # normal t-tests against 0
    print("lateral domain slopes")
    report_ttest_1_sample(lateral_domain_data.slopes)

    print("medial domain slopes")
    report_ttest_1_sample(medial_domain_data.slopes)

    print("lateral category slopes")
    report_ttest_1_sample(lateral_category_data.slopes)

    print("medial category slopes")
    report_ttest_1_sample(medial_category_data.slopes)

    # call the R script
    fpath = f"{PATHS['r_scripts']}/data/rdm_fit_slopes.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/rdm_fit_slopes_script.r {fpath}",
        shell=True,
    )


def do_stats_diffs(partition_weights):
    data = prepare_dataframe_diffs(partition_weights)

    # carry out all pairwise t-tests
    lateral_data = data[data.partitions == 0]
    medial_data = data[data.partitions == 1]
    hOc1_data = data[data.partitions == 2]

    # normal t-tests
    print("Lateral diffs vs. Medial diffs")
    report_ttest_2_sample(lateral_data.diffs, medial_data.diffs)
    print("Lateral diffs vs. hOc1 diffs")
    report_ttest_2_sample(lateral_data.diffs, hOc1_data.diffs)
    print("Medial diffs vs. hOc1 diffs")
    report_ttest_2_sample(medial_data.diffs, hOc1_data.diffs)

    # normal t-tests against 0
    print("lateral diffs")
    report_ttest_1_sample(lateral_data.diffs)
    print("medial diffs")
    report_ttest_1_sample(medial_data.diffs)
    print("hOc1 diffs")
    report_ttest_1_sample(hOc1_data.diffs)

    # call the R script
    fpath = f"{PATHS['r_scripts']}/data/rdm_fit_diffs.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/rdm_fit_diffs_script.r {fpath}",
        shell=True,
    )


def do_stats_betas(partition_weights):
    data = prepare_dataframe_betas(partition_weights)

    # call the R script
    fpath = f"{PATHS['r_scripts']}/data/rdm_fits_by_depth.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/rdm_fits_by_depth_script.r {fpath}",
        shell=True,
    )


def do_stats(partition_weights):
    do_stats_betas(partition_weights)


def main():
    """
    Wrapper for plotting functions and statistical functions
    """
    # global plot params
    plt.rcParams.update({"font.size": 20})
    r2_control_str = "_r2_control" if ARGS.r2_control else ""
    noise_str = ARGS.noise_type if ARGS.noise_type != "none" else ""
    save_dir = (
        f"{PATHS['figures']}/figure_8gh_rdm_fits_by_depth_"
        f"{ARGS.glm_dir}{noise_str}_{ARGS.thresh}{r2_control_str}"
    )
    mkdirquiet(save_dir)

    # do the RDM fits and get weights and variance explained for each partition RDM
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
    parser.add_argument("--noise_type", type=str, default="none")
    parser.add_argument(
        "--thresh", type=str, help="bias_mask_threshold to use", default="thr_75"
    )
    parser.add_argument("--r2_control", action="store_true")
    ARGS, _ = parser.parse_known_args()
    main()
