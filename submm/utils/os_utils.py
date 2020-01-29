"""
Operating system utils
"""
import os
from submm.constants import DPI

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa


def mkdirquiet(path):
    """
    Makes all directories en route to path, if the path doesn't already exist
    If it does, silently do nothing

    Inputs
        path (str): path to directory to be created
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def savefig(save_path, transparent=False):
    """
    Saves the figure with reasonable defaults
    Inputs
        save_path (str): path to save file to
        transparent (bool): if True, PNG background will be transparent (alpha = 0)
    """
    plt.savefig(save_path, dpi=DPI, bbox_inches="tight", transparent=transparent)
