"""
Figure 7A: Schematic for fitting RDMs from model RDMs
"""


# other 3rd party imports
import numpy as np

# module imports
from submm.constants import PATHS
from submm.utils.os_utils import savefig

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
        regressor = np.ones((30, 30))
        xx, yy = np.meshgrid(indices, indices)
        regressor[xx == yy] = 0

        regressors.append(regressor)

    if add_intercept:
        ones_matrix = np.ones((30, 30))
        regressors.append(ones_matrix)

    return np.array(regressors)


def main():
    """
    Wrapper for plotting functions and statistical functions
    """
    # global plot params
    plt.rcParams.update({"font.size": 34})

    regressors = build_regressors()

    fig, axes = plt.subplots(figsize=(12, 3), ncols=4)
    for regressor, ax in zip(regressors, axes):
        ax.imshow(regressor, cmap="gray_r", clim=[-0.5, 1])
        ax.axis("off")

    save_path = f"{PATHS['figures']}/figure_7a_rdm_fit_diagram.png"
    savefig(save_path)
    plt.close(fig)


if __name__ == "__main__":
    main()
