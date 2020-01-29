"""
Plotting utility functions
"""

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from sklearn.manifold import MDS
from scipy.spatial import procrustes

from submm.utils.stats import sem
from submm.constants import CATEGORY_COLORS

# define colormap to be imported elsewhere
blueblackred_colors = np.array(
    [
        [0.8, 1, 1],  # cyan-white
        [0, 1, 1],  # cyan
        [0, 0, 1],  # blue
        [0, 0, 0],  # black
        [1, 0, 0],  # red
        [1, 1, 0],  # yellow
        [1, 1, 0.8],  # yellow-white
    ]
)
blueblackred = LinearSegmentedColormap.from_list("blueblackred", blueblackred_colors)


def bar_with_err(axis, x_vals, y_vec, mn_axis=1, ebar_kwargs=None, **kwargs):
    """
    Regular barplot but with standard error bars by default

    Inputs
        axis (pyplot axis)
        x_vals (np.ndarray or list): x-axis positions for the bars
        y_vec (np.ndarray or list): vector (or matrix) of y_values to take averages
            and standard errors over
        mn_axis (int): axis over which to average to get a single number per x-tick
        ebar_kwargs (dict): keyword args for error bar
        kwargs (dict): extra arguments for ax.bar()
    """

    # compute average and SEM over y_vec
    y_mn = np.mean(y_vec, axis=mn_axis)
    y_sem = sem(y_vec, axis=mn_axis)

    axis.bar(x_vals, y_mn, **kwargs)

    # add error bar
    default_ebar_kwargs = {"fmt": "", "color": "k", "zorder": 1000, "linestyle": ""}
    if ebar_kwargs is not None:
        default_ebar_kwargs.update(ebar_kwargs)
    axis.errorbar(x_vals, y_mn, y_sem, **default_ebar_kwargs)


def plot_rdms(axes, rdms, cmap=None, clim=None, add_titles=False):
    """
    Plots each RDM on a different axis

    Inputs
        axes (np.ndarray of pyplot subplots)
        rdms (dict): keys are strings describing the RDM, values are N x N matrices
        cmap (pyplot colormap): string or colormap instance, defaults to blueblackred
        clim (tuple or list): colormap limits to clamp range, defaults to [0, 2]
            which is the full range
        add_titles (bool): if True, plots keys from rdms dict as titles above each RDM
    """

    # input sanitation
    if len(axes) > 1:
        assert len(axes) == len(rdms.keys()), "number of axes and rdms does not match"

    if cmap is None:
        cmap = blueblackred

    if clim is None:
        clim = [0, 2]

    # plot each RDM on its own axis
    for ax, (rdm_name, rdm) in zip(axes, rdms.items()):
        ax.imshow(rdm.squeeze(), cmap=cmap, clim=clim)
        if add_titles:
            ax.set_title(rdm_name)

        ax.axis("off")


def plot_embeddings(
    axes, embeddings, point_size=110, alpha=1.0, plot_dashed_lines=False
):
    """
    Plots embedded RSMs

    Inputs
        axes (np.ndarray or list of pyplot subplots)
        embeddings (dict): keys should be 'lateral', 'medial'
        point_size (float): how large each symbol should be drawn
        alpha (float): opacity of points
        plot_dashed_lines (bool): if True, connects centroids of same-domain pairs
             with a dashed line
    """

    if len(axes) > 1:
        assert len(axes) == len(
            embeddings.keys()
        ), "number of axes and embeddings does not match"

    colors = np.repeat([CATEGORY_COLORS[i, :] for i in range(10)], 3, axis=0)
    markers = np.tile(["^", "s", "v"], 10)

    # Helper function to compute centroids for each category
    def get_centroids(emb):
        centroids = np.zeros((10, 2))
        for cat_idx in range(10):
            start = cat_idx * 3
            end = start + 3
            points = emb[start:end, :]
            centroids[cat_idx, :] = np.mean(points, axis=0)

        return centroids

    def plot_single(axis, emb, colors, markers, point_size, alpha):
        """
        Plots single member of subplot
        """
        for i in range(emb.shape[0]):
            axis.scatter(
                emb[i, 0],
                emb[i, 1],
                c=[colors[i]],
                s=point_size,
                marker=markers[i],
                alpha=alpha,
            )

        # draw centroid lines
        if plot_dashed_lines:
            centroids = get_centroids(emb)
            for idx1 in [0, 2, 4, 6, 8]:
                idx2 = idx1 + 1
                ctr1 = centroids[idx1, :]
                ctr2 = centroids[idx2, :]

                axis.plot(
                    [ctr1[0], ctr2[0]],
                    [ctr1[1], ctr2[1]],
                    c=colors[idx1 * 3],
                    linestyle="dashed",
                    linewidth=4,
                    alpha=0.4,
                )

        axis.set_xticks([])
        axis.set_yticks([])

    if len(axes) == 1:
        ax = axes[0]
        emb = embeddings[0]
        plot_single(ax, emb, colors, markers, point_size, alpha)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    else:
        for ax, emb in zip(axes, embeddings.values()):
            plot_single(ax, emb, colors, markers, point_size, alpha)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)


def embed_rsms(rsms, alignment_anchor=None, n_components=2):
    """
    computes MDS embeddings aligned to that for the anchor_key

    Inputs
        rsms (dict)
        alignment_anchor (30 x 2): positions to procrustes align to. If None, don't
            align
        n_components (int): how many dimensions to embed into
    """
    # fix random seed
    SEED = 0

    # compute embeddings
    embeddings = {}
    for rsm_name, rsm in rsms.items():
        mds_obj = MDS(n_components=n_components, random_state=SEED)
        embedding = mds_obj.fit_transform(rsm.squeeze())
        if alignment_anchor is not None:
            _, embedding, _ = procrustes(alignment_anchor, embedding)
        embeddings[rsm_name] = embedding

    return embeddings
