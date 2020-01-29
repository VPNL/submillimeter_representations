"""
Figure 1A: example of stimuli with colored borders
"""

# Repo imports
import numpy as np
import os

from submm.constants import PATHS
from submm.utils.os_utils import savefig

# MPL imports
import matplotlib

matplotlib.use("Agg")
from matplotlib.pyplot import imread  # noqa:E402
import matplotlib.pyplot as plt  # noqa:E402


def plot_img_with_border(ax, img, border_width, border_color):
    """
    Adds a colorful border to an image
    """
    img_width = img.shape[0]
    background_width = img_width + 2 * border_width
    background_shape = (background_width, background_width, 3)

    rgb_img = np.stack([img] * 3, axis=2) / 255.0
    composite_img = np.ones(background_shape)
    for channel in range(3):
        composite_img[:, :, channel] = (
            composite_img[:, :, channel] * border_color[channel]
        )

    composite_img[border_width:-border_width, border_width:-border_width, :] = rgb_img
    ax.imshow(composite_img)


def main():
    fig, axes = plt.subplots(figsize=(24, 8), ncols=5, nrows=2)

    path_base = f"{PATHS['figures_misc']}/figure_1_images"

    # these numbers correspond to the images in the downloadable fLoc dataset
    stim = [
        "word-80",
        "body-24",
        "adult-28",
        "car-64",
        "corridor-62",
        "number-59",
        "limb-49",
        "child-108",
        "instrument-50",
        "house-80",
    ]

    # colors in order of categories
    colors = (
        np.array(
            [
                [0, 0, 0],  # black
                [252, 164, 0],  # dark yellow
                [248, 51, 60],  # dark red
                [0, 0, 255],  # dark blue
                [10, 255, 0],  # dark green
                [150, 150, 150],  # gray
                [252, 195, 88],  # light yellow
                [244, 110, 116],  # light red
                [0, 0, 150],  # light blue
                [10, 150, 10],  # light green
            ]
        )
        / 255.0
    )

    image_paths = [f"{path_base}/{x}.jpg" for x in stim]
    border_width = 30  # px

    for ax, image_path, border_color in zip(axes.ravel(), image_paths, colors):
        assert os.path.isfile(image_path)
        img = imread(image_path)
        plot_img_with_border(ax, img, border_width, border_color)

        ax.axis("off")

    savefig(f"{PATHS['figures']}/figure_1a.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
