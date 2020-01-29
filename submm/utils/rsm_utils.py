"""
Utilities for reading, parsing, and manipulating RSMs
"""

import h5py
import numpy as np

from scipy.optimize import nnls, lsq_linear
from submm.constants import PARTITIONS, FSID_SESSIONS, PATHS, PRIMARY_METRIC


def load_single_rsm(
    rsm_file,
    fsid_session,
    glm_dir="GLM_vanilla",
    metric=PRIMARY_METRIC,
    noise_type="none",
    partition="VTC_lateral",
    thresh="thr_75",
):
    """
    Loads one 30x30 matrix from the .h5 file

    Inputs
        rsm_file (str): path to .h5 file to read
        fsid_session (str): string denoting a combination of FSID and session date,
            like C1051_20160212
        glm_dir (str): the name of the GLM to get data for, like 'GLM_vanilla'
        metric (str): like 'znorm', 'beta'
        partition (str): VTC_lateral, VTC_medial, or hOc1
        thresh (str): threshold string
    """
    with h5py.File(rsm_file, "r") as f:
        matrix = f["corrmats"][fsid_session][glm_dir][metric][noise_type][partition][
            thresh
        ][:]

    return matrix


def load_rsms(
    metric=PRIMARY_METRIC,
    thresh="thr_75",
    glm_dir="GLM_vanilla",
    noise_type="none",
    r2_control=False,
    partitions=PARTITIONS,
):
    """
    Retrieve correlation matrices

    Inputs
        [see documentation for load_single_rsm]
        noise_type (str): can be one of "gaussian" or "none"
        r2_control (bool): If true, load from PATHS['rsms_r2_control']
    """

    rsm_path = PATHS["rsms_r2_control"] if r2_control else PATHS["rsms"]
    rsms = {}
    for partition in partitions:
        rsms_list = []
        for fsid_session in FSID_SESSIONS:
            rsms_list.append(
                load_single_rsm(
                    rsm_path,
                    fsid_session,
                    glm_dir=glm_dir,
                    partition=partition,
                    metric=metric,
                    thresh=thresh,
                    noise_type=noise_type,
                )
            )
        rsms[partition] = np.array(rsms_list)

    return rsms


def get_lower_tri(x, with_diagonal=False):
    """
    Returns the lower triangle of a provided matrix

    Inputs
        x (np.ndarray): 2D matrix to get triangle from
        with_diagonal (bool): if True, keeps the diagonal as part of lower triangle
    """
    k = 0 if with_diagonal else -1
    return x[np.tril_indices_from(x, k=k)]


def split_by_depth(rsm):
    """
    Splits a 30x30 rsm to 3 10x10 RSMS with alternating entries

    Inputs
        rsm (30 x 30 matrix)
    """

    assert rsm.shape == (30, 30)
    superficial_indices = np.arange(0, 30, 3)
    middle_indices = np.arange(1, 30, 3)
    deep_indices = np.arange(2, 30, 3)

    superficial = rsm[superficial_indices, :]
    superficial = superficial[:, superficial_indices]

    middle = rsm[middle_indices, :]
    middle = middle[:, middle_indices]

    deep = rsm[deep_indices, :]
    deep = deep[:, deep_indices]

    return np.vstack((superficial[None, :], middle[None, :], deep[None, :]))


def fit_rdm(rdm, regressors, method="lsq"):
    """
    Inputs:
        rdm: (N x N matrix)
        regressors (m, N, N): a set of m predictor matrices
        method (str):
            nnls: uses scipy.optimize.nnls
            lsq: uses scipy.optimize.lsq_linear (default)
    """

    y = rdm.flatten()
    X = np.array([x.flatten() for x in regressors]).T

    if method == "nnls":
        weights, _ = nnls(X, y)
    elif method == "lsq":
        result = lsq_linear(X, y)
        weights = result.x
    else:
        raise Exception(f"Method {method} not recognized")

    return weights
