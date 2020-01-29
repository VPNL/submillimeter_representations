"""
Computes split half reliability for the 30 x 30 RSMs
"""

import numpy as np

from submm.constants import PATHS, FSID_SESSIONS, PARTITIONS
from submm.utils.rsm_utils import load_rsms
from submm.utils.stats import report_ttest_1_sample, report_ttest_2_sample


def reliability(matrix):
    """
    Reliability is the mean of the on-diagonal elements of the matrix
    """
    return np.mean(matrix[np.diag_indices_from(matrix)])


def compute_reliability_full(corrmats):
    """
    Computes reliability for 30 x 30 matrices
    """
    reliabilities = {}
    for partition_name, partition_corrmats in corrmats.items():
        rel = np.array([reliability(x) for x in partition_corrmats])
        print(f"Testing reliability in {partition_name} against 0.0")
        report_ttest_1_sample(rel, print_mean_var=True)

        reliabilities[partition_name] = rel

    # paired t-test for lateral and medial
    print(f"Testing reliability between lateral and medial")
    report_ttest_2_sample(reliabilities["VTC_lateral"], reliabilities["VTC_medial"])


def main():
    """
    Entry point for analysis
    """
    rsms = load_rsms()
    compute_reliability_full(rsms)


if __name__ == "__main__":
    main()
