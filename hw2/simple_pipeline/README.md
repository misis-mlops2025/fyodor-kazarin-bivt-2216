# simple_pipeline

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

A short description of the project.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         simple_pipeline and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── simple_pipeline   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes simple_pipeline a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

## DVC Pipeline

This project uses DVC (Data Version Control) for managing data and model versions.

### Setup

1. Initialize DVC (if not already done):
   ```bash
   make dvc-init
   ```

2. Configure local storage (already configured in `.dvc/config`):
   - Local cache directory: `.dvc/cache`
   - All data files and models are stored locally

### Usage

- **Run entire pipeline**: `make dvc` or `dvc repro`
- **Run specific stage**: `make dvc-stage STAGE=generate_data` or `dvc repro generate_data`
- **Check pipeline status**: `make dvc-status` or `dvc status`
- **Push to local storage**: `make dvc-push` or `dvc push`
- **Pull from local storage**: `make dvc-pull` or `dvc pull`
- **Check cache size**: `make dvc-cache-size`
- **Clean cache**: `make dvc-cache-clean` or `dvc cache clean`

### Pipeline Stages

1. **generate_data**: Generates classification dataset
   - Outputs: `data/raw/classification_*.csv`
   - Tracks: `config.yaml` parameters

2. **train**: Trains ML model
   - Dependencies: Generated data, training code
   - Outputs: `models/trained_model.pkl`
   - Metrics: `metrics.json` (accuracy, precision, recall, f1_score)
   - Tracks: `config.yaml` parameters

### Local Storage

Data and models are stored in `.dvc/cache/` directory. This directory is gitignored but DVC tracks the file hashes. The actual files are stored locally and can be versioned through DVC.

--------

