from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor

from simple_pipeline.modeling.predict import predict_batch
from simple_pipeline.config import load_config

PROJECT_ROOT = Path("/opt/airflow")

default_args = {
    "owner": "data-scientist",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "batch_inference",
    default_args=default_args,
    description="Batch inference pipeline with file sensor",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "inference", "batch"],
)

def check_file_exists():
    file_path = PROJECT_ROOT / "data" / "new_data.csv"
    exists = file_path.exists()
    if exists:
        print(f"File found: {file_path}")
    return exists

file_sensor = PythonSensor(
    task_id="wait_for_new_data",
    python_callable=check_file_exists,
    poke_interval=30,
    timeout=3600,
    mode="poke",
    dag=dag,
)

def predict_task(**context):
    print("Starting batch prediction...")
    
    config = load_config(config_path=PROJECT_ROOT / "config.yaml")
    
    input_file = PROJECT_ROOT / "data" / "new_data.csv"
    model_path = PROJECT_ROOT / config.model_output_path
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = PROJECT_ROOT / "data" / "predictions" / f"predictions_{timestamp}.csv"
    
    scaler_path = PROJECT_ROOT / "data" / "processed" / "scaler.pkl"
    
    predict_batch(
        data_path=input_file,
        model_path=model_path,
        output_path=output_path,
        scaler_path=scaler_path if scaler_path.exists() else None,
        project_root=PROJECT_ROOT,
    )
    
    print("Batch prediction completed successfully!")
    return "Prediction task completed"

def delete_source_file(**context):
    print("Deleting source file...")
    
    source_file = PROJECT_ROOT / "data" / "new_data.csv"
    
    if source_file.exists():
        source_file.unlink()
        print(f"Source file {source_file} deleted successfully")
    else:
        print(f"Source file {source_file} does not exist")
    
    return "Source file deleted"

predict = PythonOperator(
    task_id="predict",
    python_callable=predict_task,
    dag=dag,
)

delete_file = PythonOperator(
    task_id="delete_source_file",
    python_callable=delete_source_file,
    dag=dag,
)

file_sensor >> predict >> delete_file

