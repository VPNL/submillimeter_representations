"""
Compute correlations between RDMs across subjects
"""

import numpy as np

from submm.constants import PATHS, FSID_SESSIONS, PARTITIONS, PRIMARY_METRIC
from submm.utils.rsm_utils import load_rsms, get_lower_tri
from submm.utils.stats import report_ttest_1_sample, report_ttest_2_sample


def main():
    """
    Entry point for analysis
    """

    rsms = load_rsms()
    rdms = {partition: 1 - x for (partition, x) in rsms.items()}

    intersubject_corr_dict = {}
    for partition_name, partition_rdms in rdms.items():
        lower_tris = np.array(
            [
                get_lower_tri(subject_rdm, with_diagonal=True)
                for subject_rdm in partition_rdms
            ]
        )
        lower_tri_corrs = np.corrcoef(lower_tris)

        # reduce symmetric corrmat by taking lower triangle (without diagonal)
        pairwise_intersubject_corrs = get_lower_tri(lower_tri_corrs)
        intersubject_corr_dict[partition_name] = pairwise_intersubject_corrs

        print(f"Mean intersub RDM corr in {partition_name}")
        report_ttest_1_sample(pairwise_intersubject_corrs, print_mean_var=True)

    print(f"Lateral vs. medial difference")
    report_ttest_2_sample(
        intersubject_corr_dict["VTC_lateral"], intersubject_corr_dict["VTC_medial"]
    )


if __name__ == "__main__":
    main()
