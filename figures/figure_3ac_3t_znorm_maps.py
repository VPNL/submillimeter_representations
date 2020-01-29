"""
Figure 3AC: z-norm maps at different resolutions
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
    fig, axes = plt.subplots(figsize=(8, 18), nrows=3)

    image_paths = {
        "3T": (
            f"{PATHS['figures_misc']}/figure_3_images/"
            f"C1051_20161006_childVSall_depth_1.png"
        ),
        "7T": (
            f"{PATHS['figures_misc']}/figure_3_images/"
            f"C1051_20160212_childVSall_depth_1_sim2pt4.png"
        ),
        "7T_noise": (
            f"{PATHS['figures_misc']}/figure_3_images/"
            f"C1051_20160212_childVSall_depth_1_sim2pt4_noise.png"
        ),
    }

    for ax, (_, image_path) in zip(axes, image_paths.items()):
        assert os.path.isfile(image_path)
        img = imread(image_path)
        img[np.where(np.sum(img, axis=2) == 0.0)] = 1.0

        ax.imshow(img[200:-100, 50:-50, :])
        ax.axis("off")

    savefig(f"{PATHS['figures']}/figure_3ac.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
