# Batch Inference Pipeline Troubleshooting

## Issue: Pipeline Didn't Start After Copying File

### Problem
The DAG has `schedule=None`, which means it **does not run automatically**. You need to **manually trigger** it.

### Solution

**Option 1: Trigger via Airflow UI**
1. Go to http://localhost:8080
2. Find the `batch_inference` DAG
3. Toggle it ON (if paused)
4. Click the "Play" button (▶) to trigger a run
5. The sensor will then check for the file

**Option 2: Trigger via CLI**
```bash
docker-compose run --rm airflow-cli airflow dags trigger batch_inference
```

### Important Notes

1. **File must be named exactly**: `new_data.csv` (not `to_predict.csv`)
2. **File location**: 
   - Host: `./data/new_data.csv`
   - Container: `/opt/airflow/data/new_data.csv`
3. **DAG must be triggered manually** because `schedule=None`
4. **Sensor checks every 30 seconds** once the DAG run starts

### Workflow

1. Copy file: `cp to_predict.csv data/new_data.csv`
2. Trigger DAG manually (UI or CLI)
3. Sensor detects file within 30 seconds
4. Pipeline processes the file
5. Results saved to `data/predictions/predictions_TIMESTAMP.csv`
6. Source file deleted

### Verify File is Visible in Container

```bash
docker-compose exec airflow-worker ls -la /opt/airflow/data/new_data.csv
```

### Check Sensor Logs

```bash
docker-compose logs -f airflow-worker | grep "wait_for_new_data"
```

### Alternative: Make DAG Auto-Trigger

If you want the DAG to automatically check for files periodically, change the schedule in `dags/batch_inference_dag.py`:

```python
schedule=timedelta(minutes=5),  # Check every 5 minutes
```

But manual trigger is recommended for batch inference workflows.

