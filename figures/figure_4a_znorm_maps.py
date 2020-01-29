"""
Figure 4A: right hemisphere VTC maps
"""
# Repo imports
import os

import numpy as np
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

    # define bounding box for right VTC
    width = 225
    y_start = 245
    x_start = 50
    bbox = [y_start, x_start, width, width]

    # first figure: betas for each predictor
    fig, axes = plt.subplots(figsize=(27.7, 8), ncols=5, nrows=2)

    # redefining contrast order to match figures
    contrasts = [
        "wordVSall",
        "bodyVSall",
        "adultVSall",
        "carVSall",
        "corridorVSall",
        "numberVSall",
        "limbVSall",
        "childVSall",
        "instrumentVSall",
        "corridorVSall",
    ]

    for contrast, ax in zip(contrasts, axes.ravel()):
        image_path = (
            f"{PATHS['figures_misc']}/figure_4_images/"
            f"C1051_20160212_{contrast}_depth_1.png"
        )

        assert os.path.isfile(image_path)
        img = imread(image_path)
        img[np.where(np.sum(img, axis=2) == 0.0)] = 1.0

        ax.imshow(img[bbox[0] : bbox[0] + bbox[2], bbox[1] : bbox[1] + bbox[3], :])
        ax.axis("off")

    savefig(f"{PATHS['figures']}/figure_4a.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
