"""
Compute correlations between RDMs from different ROIs
"""

import numpy as np

from submm.constants import PATHS, FSID_SESSIONS, PARTITIONS
from submm.utils.rsm_utils import load_rsms, get_lower_tri
from submm.utils.stats import report_ttest_1_sample, report_ttest_2_sample


def main():
    """
    Entry point for analysis
    """

    rsms = load_rsms()
    rdms = {name: 1 - rsm for (name, rsm) in rsms.items()}

    partition_pairs = {
        "lateral-medial": ["VTC_lateral", "VTC_medial"],
        "lateral-V1": ["VTC_lateral", "hOc1"],
        "medial-V1": ["VTC_medial", "hOc1"],
    }

    pair_corrs = {}
    for name, pair in partition_pairs.items():
        rdms_a = rdms[pair[0]]
        rdms_b = rdms[pair[1]]

        subject_corrs = []
        for a, b in zip(rdms_a, rdms_b):
            lower_tri_a = get_lower_tri(a)
            lower_tri_b = get_lower_tri(b)
            corr = np.corrcoef(np.stack((lower_tri_a, lower_tri_b)))[0, 1]
            subject_corrs.append(corr)

        print(f"\nCorrelations between {pair[0]} and {pair[1]}")
        pair_corrs[name] = np.array(subject_corrs)
        report_ttest_1_sample(np.array(subject_corrs), print_mean_var=True)

    print(f"\nt-test between lateral-medial and lateral-V1")
    report_ttest_2_sample(pair_corrs["lateral-medial"], pair_corrs["lateral-V1"])

    print(f"\nt-test between lateral-medial and medial-V1")
    report_ttest_2_sample(pair_corrs["lateral-medial"], pair_corrs["medial-V1"])


if __name__ == "__main__":
    main()
