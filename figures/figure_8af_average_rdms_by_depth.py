"""
Figure 8AF: Group-averaged RDMs for 10x10 (depth separated)
"""
# Repo imports
import numpy as np

from submm.constants import PATHS, PARTITIONS
from submm.utils.rsm_utils import load_rsms, split_by_depth
import submm.utils.plot_utils as plot_utils
from submm.utils.os_utils import savefig, mkdirquiet

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402
import matplotlib.cm  # noqa:E402


def main():
    """
    Entry point for script
    """
    save_dir = f"{PATHS['figures']}/figure_8af_rdms_by_depth"
    mkdirquiet(save_dir)

    # define some colormaps and limits here for each metric (maybe move to constants?)
    plot_params = {
        "tstat": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "zscore": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "znorm": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
    }

    for metric in plot_params.keys():
        print(f"Plotting metric: {metric}")
        rsms = load_rsms(metric=metric)
        mean_rdms_by_depth = {
            partition: np.mean(
                [1 - split_by_depth(rsm) for rsm in partition_rsms], axis=0
            )
            for (partition, partition_rsms) in rsms.items()
        }

        base = 6
        fig, axes = plt.subplots(figsize=(base * 3, base * 2), nrows=2, ncols=3)

        for partition_idx, partition in enumerate(PARTITIONS):
            if partition == "hOc1":
                continue
            rdm_dict = {
                f"{partition}_{x}": mean_rdms_by_depth[partition][x] for x in range(3)
            }

            plot_utils.plot_rdms(
                axes[partition_idx, :],
                rdm_dict,
                cmap=plot_params[metric]["cmap"],
                clim=plot_params[metric]["clim"],
            )

        savefig(f"{save_dir}/{metric}.png")
        plt.close(fig)


if __name__ == "__main__":
    main()
