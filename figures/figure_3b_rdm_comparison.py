"""
Figure 3B: 3T 2.4mm vs. 7T Simulated 2.4mm RDMs
"""

# Repo imports
from submm.constants import PATHS, PARTITIONS, DPI
from submm.utils.rsm_utils import load_single_rsm
from submm.utils.plot_utils import plot_rdms

# MPL imports
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa:E402


def load_rdms():
    """
    Retrieve distance matrices for "true" (3T 2.4mm) and "simulated" (7T
        downsampled 2.4mm) data
    """

    sessions = {
        "true": {"fsid_session": "C1051_20161006", "glm_dir": "GLM_vanilla"},
        "simulated": {
            "fsid_session": "C1051_20160212",
            "glm_dir": "GLM_vanilla_sim2pt4",
        },
    }

    rdms = {}
    for session_name, session_info in sessions.items():
        rdms[session_name] = {}
        for partition in PARTITIONS:
            rsm = load_single_rsm(
                PATHS["rsms"],
                session_info["fsid_session"],
                glm_dir=session_info["glm_dir"],
                partition=partition,
            )
            rdms[session_name][partition] = 1 - rsm

    return rdms


def main():
    """
    Entry point for script
    """
    rdms = load_rdms()

    fig, axes = plt.subplots(figsize=(18, 12), nrows=2, ncols=3)
    plot_rdms(axes[0], rdms["true"])
    plot_rdms(axes[1], rdms["simulated"])

    for ax in axes.ravel():
        ax.axis("off")

    plt.savefig(f"{PATHS['figures']}/figure_3b.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
