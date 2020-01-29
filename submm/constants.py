"""
Holds parameters common to many analysis scripts
"""

import numpy as np

base = (
    "/Users/eshed/projects/submillimeter_representations"
)  # modify this to point to git root
outputs_path = f"{base}/analyses/analysis_outputs"

PATHS = {
    "rsms": f"{outputs_path}/corrmats.mat",
    "rsms_r2_control": f"{outputs_path}/corrmats_r2_control.mat",
    "rsms_6depth": f"{outputs_path}/corrmats_6depth.mat",
    "metric_means": f"{outputs_path}/metric_means.mat",
    "metric_means_r2control": f"{outputs_path}/metric_means_r2control.mat",
    "tsnr": f"{outputs_path}/tsnr.mat",
    "r2": f"{outputs_path}/r_squared.mat",
    "figures": f"{base}/figures/python_outputs",
    "figures_misc": f"{base}/figures/figures_misc",
    "r_scripts": f"{base}/stats/R_scripts",
}

# statistical threshold
ALPHA = 0.05

# figure saving resolution
DPI = 300

# subjects to use in analysis
FSIDs = ["C1051", "CVNS104", "CVNS103", "CVNS105", "CVNS109", "CVNS011", "CVNS012"]

# dataset names
DATASETS = [
    "20160212-ST001-E002",
    "20160623-CVNS004-fLoc_ph",
    "20160628-CVNS003-fLoc_ph",
    "20160630-CVNS005-fLoc_ph",
    "20161014-ST001-CVNS009Floc",
    "20170316-ST001-CVNS011Floc",
    "20170316-ST001-CVNS012Floc",
]

# combinations of FSID and dataset date
FSID_SESSIONS = [
    "C1051_20160212",
    "CVNS104_20160623",
    "CVNS103_20160628",
    "CVNS105_20160630",
    "CVNS109_20161014",
    "CVNS011_20170316",
    "CVNS012_20170316",
    # "C1051_20161006", # 3T session
]

# order of contrasts to use
CONTRASTS = [
    "numberVSall",
    "wordVSall",
    "limbVSall",
    "bodyVSall",
    "adultVSall",
    "childVSall",
    "carVSall",
    "instrumentVSall",
    "houseVSall",
    "corridorVSall",
]

CATEGORY_COLORS = (
    np.array(
        [
            [0, 0, 0],  # black
            [150, 150, 150],  # gray
            [252, 164, 0],  # dark yellow
            [252, 195, 88],  # light yellow
            [248, 51, 60],  # dark red
            [244, 110, 116],  # light red
            [0, 0, 255],  # dark blue
            [0, 0, 150],  # light blue
            [10, 255, 0],  # dark green
            [10, 150, 10],  # light green
        ]
    )
    / 255.0
)

DOMAIN_COLORS = (
    np.array(
        [
            [0, 0, 0],  # black
            [252, 164, 0],  # dark yellow
            [248, 51, 60],  # dark red
            [0, 0, 255],  # dark blue
            [10, 255, 0],  # dark green
        ]
    )
    / 255.0
)

PARTITION_COLORS = ["#377eb8", "#e41a1c", "#BBBBBB"]
PARTITION_NAMES = ["Lateral\nVTC", "Medial\nVTC", "V1"]

# which metrics to iterate over in analysis scripts
METRICS = ["tstat", "zscore", "znorm"]

# main metric that, e.g., RDM fits should be computed for
PRIMARY_METRIC = "znorm"

# partitions (or ROIs) to analyze
PARTITIONS = ["VTC_lateral", "VTC_medial", "hOc1"]
