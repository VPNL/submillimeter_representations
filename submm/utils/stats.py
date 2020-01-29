"""
Statistical utilities
"""

import numpy as np
import scipy.stats as ss


def sem(vals, axis=0):
    """
    Computes standard error of the mean
    """
    return np.std(vals, axis=axis) / np.sqrt(vals.shape[axis])


def report_mn_sem(x):
    """
    Reports mean and standard deviation of a vector, x
    """
    x = np.array(x)
    print(f"{np.mean(x):.3f} +/- {np.std(x) / np.sqrt(x.shape[0]):.3f}")


def report_ttest_2_sample(x, y, print_mean_var=False):
    """
    Reports results of a 2-sample matched pairs t test
    """
    t, p = ss.ttest_rel(x, y)
    df = x.shape[0] - 1

    mu_x = x.mean()
    sem_x = sem(x)

    mu_y = y.mean()
    sem_y = sem(y)

    if print_mean_var:
        print(f"{mu_x:.3} +/- {sem_x:.3} vs. {mu_y:.3} +/- {sem_y:.3}")
    print(f"t({df}) = {t:.3}, p = {p:.3}")


def report_ttest_1_sample(x, population_mean=0.0, print_mean_var=False):
    """
    Reports results of a 2-sample matched pairs t test

    Inputs:
        x (array): vector whose mean is to be compared against the population mean
        population_mean (float): the mean against which to compare the mean of x
        print_mean_var (bool): whether or not to also print mean and variance of x
    """
    t, p = ss.ttest_1samp(x, population_mean)
    df = x.shape[0] - 1

    mu_x = x.mean()
    sem_x = sem(x)

    if print_mean_var:
        print(f"{mu_x:.2} +/- {sem_x:.3}")
    print(f"t({df}) = {t:.3}, p = {p:.3}")
