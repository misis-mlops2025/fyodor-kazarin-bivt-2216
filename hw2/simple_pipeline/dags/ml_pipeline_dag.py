from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator

from simple_pipeline.dataset import generate_classification_dataset
from simple_pipeline.preprocessing import preprocess_data
from simple_pipeline.modeling.train import train_model
from simple_pipeline.config import load_config


default_args = {
    "owner": "data-scientist",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

PROJECT_ROOT = Path("/opt/airflow")


def data_generation_task(**context):
    print("Starting data generation...")
    
    generate_classification_dataset(
        n_samples=1000,
        n_features=20,
        n_informative=10,
        n_redundant=5,
        n_classes=2,
        random_state=42,
        output_dir=PROJECT_ROOT / "data" / "raw",
    )
    
    print("Data generation completed successfully!")
    return "Data generation task completed"


def preprocessing_task(**context):
    print("Starting preprocessing...")
    
    raw_data_path = PROJECT_ROOT / "data" / "raw" / "classification_dataset.csv"
    output_path = PROJECT_ROOT / "data" / "processed" / "classification_dataset.csv"
    
    preprocess_data(
        raw_data_path=raw_data_path,
        output_path=output_path,
        project_root=PROJECT_ROOT,
    )
    
    print("Preprocessing completed successfully!")
    return "Preprocessing task completed"


def model_training_task(**context):
    print("Starting model training...")
    
    config = load_config(config_path=PROJECT_ROOT / "config.yaml")
    
    config.data_path = PROJECT_ROOT / "data/processed/classification_dataset.csv"
    
    model, accuracy = train_model(config=config)
    
    print(f"Model training completed successfully! Accuracy: {accuracy:.4f}")
    return f"Model training task completed with accuracy: {accuracy:.4f}"


dag = DAG(
    "ml_pipeline",
    default_args=default_args,
    description="ML Pipeline: Data Generation -> Preprocessing -> Model Training",
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "classification", "pipeline"],
)

generate_data = PythonOperator(
    task_id="data_generation",
    python_callable=data_generation_task,
    dag=dag,
)

preprocess = PythonOperator(
    task_id="preprocessing",
    python_callable=preprocessing_task,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id="model_training",
    python_callable=model_training_task,
    dag=dag,
)

generate_data >> preprocess >> train_model_task

