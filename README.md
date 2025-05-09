# 2d-RDK Experiment Analysis

This repository contains the analysis files for the research work: **Integration of information in the perceptual decision making task**.

Detailed description and goals of the experiment can be found here: https://osf.io/4dn65

## Experiment

The script for running experiments is in `experiment` folder with some details on how it was performed.

## Data

The anonymised data collected in this experiment is shared publicly (CC by 4.0) here:
https://figshare.com/articles/dataset/13567916

## Procedure

Some packages needed to run the analysis:

```
pandas >= 1.0.5
numpy >= 1.19.1
scipy >= 1.5.0
pingouin >= 0.3.8
matplotlib >= 3.2.2
seaborn >= 0.11.0
```

This assumes Python 3.7.

Additionally, we used [HDDM python](http://ski.clps.brown.edu/hddm_docs/) package for HDDM modelling, which requires Python 2.7.

The data needs to be stored in the `selected/` folder (it indicates "selected" participants that passed quality control criteria of the experiment).

Some functionality of this procedure is automatically tested with `pytest`.

The files should be run in the following order:

1. `data_analysis.ipynb` - behavioural data analysis, creates plots and files needed for further HDDM analysis or JASP statistical tests.
2. `hddm_run.py` - runs HDDM models with different settings.
3. `hddm_analysis.ipynb`, `hddm_model_comparison.ipynb` - compare HDDM models and make plots.
4. `grid_ww_iter.py` (optionally: `grid_cluster.sh`) - runs grid search of parameters of modified Wong&Wang model.
5. `grid_viz.py` - visualises grid plot from the previous step.

## Running with Docker

For convenience, there is a Docker image that makes it easy to install all dependencies.

Run the following to build the image:

```sh
$ docker build -t 2drdk .
```

And this to mount the current folder and run the jupyter-lab with all packages installed. There are two ipython kernels: 
(a) main for data analysis and grid search (Python 3.7)
(b) `hddm` for HDDM fitting (Python 2.7).

```sh
$ docker run -p 8888:8888 -v $(pwd):/usr/src/app 2drdk
```

## Citation

Please, cite the article below, if any of this work was helpful.

```

@article{krzeminski_2ddm_2022,
	title = {Imperfect integration: {Congruency} between multiple sensory sources modulates decision-making processes},
	issn = {1943-393X},
	doi = {10.3758/s13414-021-02434-7},
	journal = {Attention, Perception, \& Psychophysics},
	author = {Krzemiński, Dominik and Zhang, Jiaxiang},
	month = apr,
	year = {2022},
}
```
