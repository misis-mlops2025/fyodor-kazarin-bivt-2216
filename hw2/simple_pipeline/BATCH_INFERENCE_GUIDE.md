# Batch Inference Pipeline - File Location Guide

## Which Container Runs the Sensor?

The **PythonSensor** task runs on the **`airflow-worker`** container because:
- Your setup uses `CeleryExecutor` (see docker-compose.yaml line 58)
- With CeleryExecutor, all tasks (including sensors) execute on the worker container
- The scheduler only schedules tasks, it doesn't execute them

## Where to Copy the File

Since all Airflow containers share the same volume mount from the host:

**Copy the file to the HOST directory:**
```bash
cp your_data.csv /home/fydor/Programming/fyodor-kazarin-bivt-2216/hw2/simple_pipeline/data/new_data.csv
```

This file will be visible inside ALL containers as:
```
/opt/airflow/data/new_data.csv
```

## Volume Mount Details

From docker-compose.yaml, the volume mount is:
```yaml
- ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
```

This means:
- **Host path**: `./data` (relative to docker-compose.yaml location)
- **Container path**: `/opt/airflow/data`
- **Full host path**: `/home/fydor/Programming/fyodor-kazarin-bivt-2216/hw2/simple_pipeline/data/`

## Quick Test

1. **Copy your file:**
   ```bash
   cd /home/fydor/Programming/fyodor-kazarin-bivt-2216/hw2/simple_pipeline
   cp to_predict.csv data/new_data.csv
   ```

2. **Verify it's visible in the container:**
   ```bash
   docker-compose exec airflow-worker ls -la /opt/airflow/data/new_data.csv
   ```

3. **Check sensor logs:**
   ```bash
   docker-compose logs -f airflow-worker | grep "wait_for_new_data"
   ```

## Important Notes

- The sensor checks every 30 seconds (poke_interval=30)
- The sensor has a 1-hour timeout
- Once the file is detected, the pipeline will:
  1. Run predictions
  2. Save results to `data/predictions/predictions_TIMESTAMP.csv`
  3. Delete `data/new_data.csv`

- After deletion, you can place a new file with the same name to trigger another run

