### Ultra-high-resolution fMRI of human ventral temporal cortex reveals differential representation of categories and domains 
**Eshed Margalit, Keith Jamison, Kevin Weiner, Luca Vizioli, Ru-Yuan Zhang, Kendrick Kay\*, Kalanit Grill-Spector\***

\* Co-senior author

This repository contains code to analyze data, compute statistical test results, and make bits of figures that are combined later in third-party software. 

#### Overall organization :clipboard:
Code relating to figures, statistical tests, and data analyses is provided in subdirectories `figures/`, `stats/`, and `analyses/`, respectively. Each subdirectory contains a README explaining its contents, linked here:

1. [`Figures README`](figures/README.md) :bar_chart:
1. [`Statistical Analyses README`](stats/README.md) :computer:
1. [`Data Analyses README`](analyses/README.md) :microscope:

#### Dependencies :package:
The code in `figures/` and `stats/` can be run on your machine assuming the following dependencies:
```
python 3.6+
R (callable with Rscript from command line)
```

##### R packages used
```
nmle
sjstats
```

##### Running the Python code
To run the code in `figures/` and `stats/`, you must have the `submm` package installed. I recommend installing into a virtual environment.

1. From the project root directory, you can install the `submm` package with `pip install -e .`
1. Modify the project root directory in `submm/constants.py`, in particular line 7. 
1. Modify `figures/make_all.sh` to source the virtualenv you created, or delete the corresponding line if you installed into your system python.

If you want to create all of the figures (and then some!) you can run `make_all.sh`

##### Other
1. The outputs in `analyses/analysis_outputs/` are generated with the scripts from `analyses/` and provided here to make figure generation and statistical testing easy.
1. You'll need to edit `stats/params.py` and `figures/params.py` to point the scripts to the absolute path where the `analysis_outputs/` directory lives.

The code in `analyses` can not, in general, be run on your machine, as it depends on absolute paths to FreeSurfer surfaces and timeseries data. Please see the data availability statement in [Kay et al., 2019](https://www.sciencedirect.com/science/article/abs/pii/S1053811919300928) for more.

