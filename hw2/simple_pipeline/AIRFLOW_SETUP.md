# Airflow Pipeline Setup Guide

This guide explains how to set up and run the Airflow pipeline for the ML model.

## Overview

The Airflow pipeline consists of three stages:

1. **Data Generation**: Generates synthetic classification dataset
2. **Preprocessing**: Scales features and prepares data for training
3. **Model Training**: Trains the machine learning model

## Prerequisites

1. Install Apache Airflow:
   ```bash
   pip install apache-airflow
   ```

2. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Airflow Setup

1. **Initialize Airflow database** (first time only):
   ```bash
   airflow db init
   ```

2. **Create an Airflow user** (first time only):
   ```bash
   airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com \
       --password admin
   ```

3. **Set Airflow home directory** (optional, if not using default):
   ```bash
   export AIRFLOW_HOME=/path/to/airflow/home
   ```

4. **Configure Airflow to find your DAGs**:
   
   Edit `$AIRFLOW_HOME/airflow.cfg` and set:
   ```ini
   dags_folder = /home/fydor/Programming/fyodor-kazarin-bivt-2216/hw2/simple_pipeline/dags
   ```
   
   Or set the environment variable:
   ```bash
   export AIRFLOW__CORE__DAGS_FOLDER=/home/fydor/Programming/fyodor-kazarin-bivt-2216/hw2/simple_pipeline/dags
   ```

5. **Set Python path** (so Airflow can import your modules):
   ```bash
   export PYTHONPATH=/home/fydor/Programming/fyodor-kazarin-bivt-2216/hw2/simple_pipeline:$PYTHONPATH
   ```

## Running Airflow

1. **Start the Airflow webserver**:
   ```bash
   airflow webserver --port 8080
   ```

2. **Start the Airflow scheduler** (in a separate terminal):
   ```bash
   airflow scheduler
   ```

3. **Access the Airflow UI**:
   Open your browser and navigate to `http://localhost:8080`
   - Username: `admin` (or the username you created)
   - Password: `admin` (or the password you set)

## Using the Pipeline

1. **Trigger the DAG manually**:
   - In the Airflow UI, find the `ml_pipeline` DAG
   - Toggle it ON (if it's paused)
   - Click the "Play" button to trigger a run

2. **Monitor execution**:
   - Click on the DAG name to see the graph view
   - Click on individual tasks to see logs and details
   - Green = success, Red = failed, Yellow = running

3. **View task logs**:
   - Click on a task in the graph view
   - Click "Log" to see the execution logs

## Pipeline Stages

### Stage 1: Data Generation
- Generates synthetic classification dataset
- Saves to `data/raw/classification_dataset.csv`
- Creates separate feature and target files

### Stage 2: Preprocessing
- Loads raw data from `data/raw/classification_dataset.csv`
- Scales features using StandardScaler
- Saves processed data to `data/processed/classification_dataset.csv`
- Saves scaler to `data/processed/scaler.pkl`

### Stage 3: Model Training
- Loads processed data
- Trains model based on configuration in `config.yaml`
- Saves trained model to `models/trained_model.pkl`
- Outputs accuracy and classification report

## Configuration

The pipeline uses the configuration from `config.yaml`. You can modify:
- Model type (logistic_regression, random_forest, decision_tree)
- Model hyperparameters
- Data paths
- Model output path

## Troubleshooting

1. **DAG not appearing in Airflow UI**:
   - Check that `dags_folder` is set correctly
   - Check for syntax errors in the DAG file
   - Ensure `PYTHONPATH` includes the project root

2. **Import errors**:
   - Make sure `PYTHONPATH` includes the project root directory
   - Verify all dependencies are installed

3. **Task failures**:
   - Check task logs in the Airflow UI
   - Verify file paths exist
   - Check that required directories are created

## Testing the Pipeline Locally

You can test individual stages without Airflow:

```bash
# Test data generation
python -m simple_pipeline.dataset

# Test preprocessing
python -c "from simple_pipeline.preprocessing import preprocess_data; from pathlib import Path; preprocess_data('data/raw/classification_dataset.csv')"

# Test training
python -m simple_pipeline.modeling.train
```

