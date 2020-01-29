"""
Computes correlation between 3t and 7t data for C1051
"""

import numpy as np

# Repo imports
from submm.constants import PATHS, PARTITIONS
from submm.utils.rsm_utils import load_single_rsm, get_lower_tri


def load_rdms():
    """
    Retrieve distance matrices for "true" (3T 2.4mm) and "simulated" (7T downsampled
    2.4mm) data
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
            rdms[session_name][partition] = get_lower_tri(1 - rsm, with_diagonal=True)

    return rdms


def main():
    """
    Entry point for analysis
    """

    rdm_lower_triangles = load_rdms()

    # compute correlations
    for partition in PARTITIONS:
        corr = np.corrcoef(
            rdm_lower_triangles["true"][partition],
            rdm_lower_triangles["simulated"][partition],
        )[0, 1]
        print(
            (
                f"Correlation between lower triangles of 3T and 7T RDMs is {corr:.2f}"
                f"in {partition}"
            )
        )


if __name__ == "__main__":
    main()
