# Running Airflow Pipeline with Docker Compose

## Quick Start

1. **Set up environment** (first time only):
   ```bash
   cd /home/fydor/Programming/fyodor-kazarin-bivt-2216/hw2/simple_pipeline
   echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_PROJ_DIR=." > .env
   ```

2. **Initialize Airflow** (first time only):
   ```bash
   docker-compose up airflow-init
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Access Airflow UI**:
   - Open http://localhost:8080
   - Login: `airflow` / `airflow`

5. **Run the pipeline**:
   - Find the `ml_pipeline` DAG in the UI
   - Toggle it ON (if paused)
   - Click the play button (▶) to trigger a run

## Useful Commands

**View logs:**
```bash
docker-compose logs -f
```

**View logs for specific service:**
```bash
docker-compose logs -f airflow-scheduler
docker-compose logs -f airflow-worker
```

**Stop all services:**
```bash
docker-compose down
```

**Stop and remove volumes (clean slate):**
```bash
docker-compose down -v
```

**Restart a specific service:**
```bash
docker-compose restart airflow-scheduler
```

**Check service status:**
```bash
docker-compose ps
```

**Access Airflow CLI:**
```bash
docker-compose run --rm airflow-cli airflow dags list
docker-compose run --rm airflow-cli airflow dags trigger ml_pipeline
```

## Troubleshooting

**DAG not appearing:**
- Check logs: `docker-compose logs airflow-scheduler`
- Verify DAG file syntax: `docker-compose run --rm airflow-cli airflow dags list-import-errors`

**Import errors:**
- Ensure `simple_pipeline` directory is mounted (check docker-compose.yaml volumes)
- Check PYTHONPATH is set in environment variables

**Task failures:**
- Check task logs in Airflow UI
- View worker logs: `docker-compose logs airflow-worker`

**Permission issues:**
- Ensure AIRFLOW_UID in .env matches your user ID: `id -u`


