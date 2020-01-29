"""
Figure 5: Hypothetical RDM/MDS embeddings
"""

from sklearn.manifold import MDS
import numpy as np

from submm.constants import PATHS, DPI
import submm.utils.plot_utils as plot_utils

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402


def plot_RDM(ax, level):
    """
    Here the values are not set to 0 and 1 (as they are everywhere else)
    because white/black makes it hard to see the structure. Instead, we show
    gray and black here.
    """
    xx, yy = np.meshgrid(level["level"], level["level"])
    base = np.ones((30, 30)) * 0.5
    base[xx == yy] = 1
    ax.imshow(base, cmap="gray", clim=(0, 1))

    for i in range(31):
        ax.axvline(i - 0.5, color="k")
        ax.axhline(i - 0.5, color="k")
    ax.set_xlim((-0.51, 29.51))
    ax.axis("off")


def plot_MDS(ax, level, plot_dashed_lines=False):
    mds = MDS(n_components=2)

    xx, yy = np.meshgrid(level["level"], level["level"])
    base = np.zeros((30, 30))
    base[xx == yy] = 0.5

    np.random.seed(level["seed"])
    pos = mds.fit_transform(base + np.random.random(size=(30, 30)) * level["noise"])

    plot_utils.plot_embeddings(
        [ax], [pos], point_size=250, alpha=0.8, plot_dashed_lines=plot_dashed_lines
    )


def main():
    """
    Entry point for script
    """
    depths = np.tile(np.arange(3), 10)
    domains = np.repeat(np.arange(5), 6)
    categories = np.repeat(np.arange(10), 3)

    # choose amount of noise to prevent points from perfectly overlapping
    levels = [
        {"name": "Domain", "level": domains, "seed": 0, "noise": 0.3},
        {"name": "Category", "level": categories, "seed": 0, "noise": 0.15},
        {"name": "Depth", "level": depths, "seed": 0, "noise": 0.3},
    ]

    fig, axes = plt.subplots(
        figsize=(21, 14), ncols=3, nrows=2, gridspec_kw={"hspace": 0.5}
    )

    for level_idx, level in enumerate(levels):
        plot_RDM(axes[0, level_idx], level)
        plot_MDS(axes[1, level_idx], level, plot_dashed_lines=True)

    save_path = f"{PATHS['figures']}/figure_5_hypothetical_rdm_mds.png"
    plt.savefig(save_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
