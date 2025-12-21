# Running Feast with Docker

This directory contains a docker-compose setup for running Feast locally in a containerized environment.

## Prerequisites

- Docker and Docker Compose installed

## Starting the Environment

```bash
docker-compose up -d
```

This will start a container with Feast installed and mount the current directory to `/feast-project` inside the container.

## Using Feast

Enter the container to run Feast commands:

```bash
docker exec -it feast-dev bash
```

Once inside the container, you can run standard Feast commands:

```bash
# Apply feature definitions
feast apply

# Materialize features to the online store
feast materialize-incremental

# Run the test workflow
python test_workflow.py
```

## Stopping the Environment

```bash
docker-compose down
```

## Notes

- All data files (registry.db, online_store.db) are stored locally in the `data/` directory and will persist between container restarts
- Changes to feature definitions will be immediately reflected in the container due to volume mounting
