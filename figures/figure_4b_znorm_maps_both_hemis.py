"""
Figure 4B: both hemisphere maps for C1051 at each depth
"""

# Repo imports
import numpy as np
import os

from submm.constants import PATHS, PRIMARY_METRIC
from submm.utils.os_utils import savefig

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402
from matplotlib.pyplot import imread  # noqa:E402


def main():
    """
    Entry point for script
    """

    # first figure: betas for each predictor
    fig, axes = plt.subplots(figsize=(16, 8), ncols=3, nrows=1)

    for depth, ax in zip(range(1, 4), axes.ravel()):
        image_path = (
            f"{PATHS['figures_misc']}/figure_4_images/"
            f"C1051_20160212_adultVSall_depth_{depth}.png"
        )

        assert os.path.isfile(image_path)
        img = imread(image_path)
        img[np.where(np.sum(img, axis=2) == 0.0)] = 1.0

        ax.imshow(img[200:-100, 50:-50, :])
        ax.axis("off")

    savefig(f"{PATHS['figures']}/figure_4b.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
