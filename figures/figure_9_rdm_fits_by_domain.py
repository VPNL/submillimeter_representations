"""
Figure 9: RDM fits by domain
Note these aren't actually "fits", we're just averaging different bits of the RDM
"""

# other 3rd party imports
import numpy as np
import pandas as pd

# python imports
import argparse
import subprocess

# module imports
from submm.constants import PATHS, PARTITIONS, DOMAIN_COLORS
from submm.utils.rsm_utils import load_rsms, split_by_depth
from submm.utils.os_utils import savefig
from submm.utils.plot_utils import bar_with_err

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402


def plot_partition_weights(axes, partition_weights):
    """
    Produces plot showing fit betas for each partition across subjects
    """

    # x positions for each domain to start at
    domain_starts = [0, 9, 18, 27, 36]

    # x offsets for each depth, e.g., superficial aligns with domain_start for
    # that domain
    depth_bonus = [0, 3, 6]
    for (partition, weights), ax in zip(partition_weights.items(), axes):
        if partition == "hOc1":
            continue
        for domain_idx in range(5):
            domain_specific_weights = weights[:, :, domain_idx, :]
            ebar_kwargs = {"color": DOMAIN_COLORS[domain_idx], "linewidth": 2}
            for depth in range(3):
                depth_specific_weights = domain_specific_weights[:, depth, :]

                # compute where to put this bar
                x_value = domain_starts[domain_idx] + depth_bonus[depth]

                bar_with_err(
                    ax,
                    x_value,
                    depth_specific_weights[:, 0],
                    facecolor=DOMAIN_COLORS[domain_idx],
                    mn_axis=0,
                    ebar_kwargs=ebar_kwargs,
                )
                bar_with_err(
                    ax,
                    x_value + 1,
                    depth_specific_weights[:, 1],
                    facecolor="none",
                    edgecolor=DOMAIN_COLORS[domain_idx],
                    mn_axis=0,
                    ebar_kwargs=ebar_kwargs,
                )

        ax.set_xticks([3.5, 12.5, 21.5, 30.5, 39.5])
        ax.set_xticklabels(["Characters", "Bodies", "Faces", "Objects", "Places"])

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel("Mean Dissimilarity")
        # ax.set_title(partition)


def prepare_dataframe(partition_weights, roi_indices=None):

    partitions_list = []
    subjects_list = []
    domains_list = []
    wb_membership_list = []
    depth_list = []
    values_list = []

    if roi_indices is None:
        roi_indices = np.arange(2)

    for partition_idx, (partition_name, weights) in enumerate(
        partition_weights.items()
    ):
        if partition_idx not in roi_indices:
            continue

        for depth_idx in range(3):
            depth_weights = weights[:, depth_idx, :, :]

            for domain_idx in range(5):
                domain_specific_weights = depth_weights[:, domain_idx, :]

                for wb_membership_idx in range(2):
                    values = domain_specific_weights[:, wb_membership_idx]

                    for sub_idx in range(values.shape[0]):
                        partitions_list.append(partition_idx)
                        subjects_list.append(sub_idx)
                        domains_list.append(domain_idx)
                        wb_membership_list.append(wb_membership_idx)
                        depth_list.append(
                            depth_idx - 1
                        )  # subtract one to center continuous regressor
                        values_list.append(values[sub_idx])

    partitions_list = np.array(partitions_list)
    subjects_list = np.array(subjects_list)
    domains_list = np.array(domains_list)
    wb_membership_list = np.array(wb_membership_list)
    depth_list = np.array(depth_list)
    values_list = np.array(values_list)

    data = {
        "partitions": partitions_list,
        "subjects": subjects_list,
        "domains": domains_list,
        "wb_membership": wb_membership_list,
        "depth": depth_list,
        "values": values_list,
    }

    return pd.DataFrame(data=data)


def get_partition_weights(glm_dir="GLM_vanilla", noise_type="none"):
    rsms = load_rsms(glm_dir=glm_dir, noise_type=noise_type)
    rdms_by_depth = {
        partition: np.array([1 - split_by_depth(rsm) for rsm in partition_rsms])
        for (partition, partition_rsms) in rsms.items()
    }

    # fit domain, category, and depth weights to each rdm
    partition_weights = {}
    for partition in PARTITIONS:
        partition_rdms = rdms_by_depth[partition]
        subject_weights = []

        for subject_rdms in partition_rdms:
            depth_weights = []

            for depth_rdm in subject_rdms:
                domain_weights_list = []

                for domain_idx in range(5):
                    start = domain_idx * 2
                    end = start + 2
                    domain_rdm = depth_rdm[start:end, start:end]

                    within_category_mean = np.mean((domain_rdm[0, 0], domain_rdm[1, 1]))
                    between_category_mean = np.mean(
                        (domain_rdm[0, 1], domain_rdm[1, 0])
                    )

                    domain_weights_list.append(
                        [within_category_mean, between_category_mean]
                    )

                depth_weights.append(np.stack(domain_weights_list))
            subject_weights.append(np.stack(depth_weights))
        partition_weights[partition] = np.stack(subject_weights)

    return partition_weights


def make_plots(partition_weights, savepath):
    # first figure: betas for each predictor
    fig, axes = plt.subplots(figsize=(10, 6), nrows=2, sharey=True, sharex=True)
    plot_partition_weights(axes, partition_weights)

    savefig(savepath)
    plt.close(fig)


def main():
    """
    Wrapper for plotting functions and statistical functions
    """
    # global plot params
    plt.rcParams.update({"font.size": 16})

    noise_str = ARGS.noise_type if ARGS.noise_type != "none" else ""
    savepath = (
        f"{PATHS['figures']}/figure_9_fits_by_domain_{ARGS.glm_dir}{noise_str}.png"
    )
    args_kv_pairs = vars(ARGS)
    partition_weights = get_partition_weights(**args_kv_pairs)

    # make and save plots
    make_plots(partition_weights, savepath)

    data = prepare_dataframe(partition_weights)
    # call the R script

    fpath = f"{PATHS['r_scripts']}/data/fits_by_domain.csv"
    data.to_csv(fpath)
    subprocess.call(
        f"Rscript --vanilla {PATHS['r_scripts']}/fits_by_domain_script.r {fpath}",
        shell=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--glm_dir", type=str, help="GLM type to use", default="GLM_vanilla"
    )
    parser.add_argument("--noise_type", type=str, default="none")
    ARGS, _ = parser.parse_known_args()
    main()
