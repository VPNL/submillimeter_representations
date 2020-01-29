"""
Figure 6: Group-averaged RDMs and MDS embeddings for 30x30 RDMs
"""

# Repo imports
import numpy as np
from sklearn.manifold import MDS

from submm.constants import PATHS
from submm.utils.rsm_utils import load_rsms
import submm.utils.plot_utils as plot_utils
from submm.utils.os_utils import mkdirquiet, savefig

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402
import matplotlib.cm  # noqa:E402


def get_MDS_anchor(rsms, partition="VTC_lateral", participant_idx=0):
    """
    Indicates with partition and subject to use as the "anchor" to align
    all MDS embeddings to. Defaults to lateral VTC in participant S1
    """
    reference_rsm = rsms[partition][participant_idx]
    mds_obj = MDS(n_components=2, random_state=0)
    anchor = mds_obj.fit_transform(reference_rsm)
    return anchor


def plot_helper(matrices, aligned_embeddings, plot_params, savepath):

    fig, axes = plt.subplots(figsize=(18, 12), nrows=2, ncols=3)
    plot_utils.plot_rdms(
        axes[0], matrices, cmap=plot_params["cmap"], clim=plot_params["clim"]
    )

    plot_utils.plot_embeddings(
        axes[1], aligned_embeddings, point_size=250, alpha=0.8, plot_dashed_lines=True
    )

    savefig(savepath)
    plt.close(fig)


def max_norm(rsm):
    orig_shape = rsm.shape
    flat_rsm = rsm.flatten()
    normed_flat_rsm = flat_rsm / np.max(np.abs(flat_rsm))
    return normed_flat_rsm.reshape(orig_shape)


def make_plots(glm_dir, save_dir):
    """
    Entry point for script
    """

    rsm_plot_params = {
        "beta": {"cmap": plot_utils.blueblackred, "clim": [0, 1]},
        "tnorm": {"cmap": plot_utils.blueblackred, "clim": [0, 1]},
        "tstat": {"cmap": plot_utils.blueblackred, "clim": [-0.5, 0.5]},
        "zscore": {"cmap": plot_utils.blueblackred, "clim": [-0.5, 0.5]},
        "znorm": {"cmap": plot_utils.blueblackred, "clim": [-0.5, 0.5]},
        "betasub": {"cmap": plot_utils.blueblackred, "clim": [-0.5, 0.5]},
    }

    rdm_plot_params = {
        "beta": {"cmap": plot_utils.blueblackred, "clim": [0, 1]},
        "tnorm": {"cmap": plot_utils.blueblackred, "clim": [0, 1]},
        "tstat": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "zscore": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "znorm": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
        "betasub": {"cmap": plot_utils.blueblackred, "clim": [0.5, 1.5]},
    }

    key_order = ["znorm", "tstat", "zscore", "betasub", "tnorm", "beta"]
    for metric in key_order:
        print(f"Plotting metric: {metric}")
        rsms = load_rsms(metric=metric, glm_dir=glm_dir)
        mds_anchor = get_MDS_anchor(rsms)

        mean_rsms = {}
        mean_rdms = {}
        for rsm_name, rsm in rsms.items():
            mean_rsms[rsm_name] = np.mean(rsm, axis=0, keepdims=True)
            mean_rdms[rsm_name] = np.mean(1 - rsm, axis=0, keepdims=True)

        # align the group-average RSMs to the mds anchor
        aligned_embeddings = plot_utils.embed_rsms(
            mean_rsms, alignment_anchor=mds_anchor
        )

        plot_helper(
            mean_rdms,
            aligned_embeddings,
            rdm_plot_params[metric],
            f"{save_dir}/{metric}_rdms.png",
        )
        plot_helper(
            mean_rsms,
            aligned_embeddings,
            rsm_plot_params[metric],
            f"{save_dir}/{metric}_rsms.png",
        )


def main():
    for glm_dir in ["GLM_vanilla", "GLM_vanilla_sim2pt4"]:
        save_dir = f"{PATHS['figures']}/figure_6_rdms_rsms_{glm_dir}"
        mkdirquiet(save_dir)
        make_plots(glm_dir, save_dir)


if __name__ == "__main__":
    main()
