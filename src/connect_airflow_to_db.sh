#!/bin/bash

# Load environment variables from the .env file
export $(grep -v '^#' .env | xargs)

# Get the PostgreSQL port number dynamically
# POSTGRES_PORT=$(docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Ports}}" | awk '$2 ~ /postgres/ {split($3, a, ":"); split(a[2], b, "-"); print b[1]}')
POSTGRES_PORT=$(docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Ports}}" | awk '$2 ~ /postgres/ {split($3, a, "->"); split(a[2], b, "/"); print b[1]}')

# Define the Airflow webserver container name
AIRFLOW_CONTAINER_NAME="ecommerce_airflow_db-airflow-webserver-1"

# Add the connection to Airflow using Docker exec
docker exec -it $AIRFLOW_CONTAINER_NAME airflow connections delete 'my_prod_db' || true
docker exec -it $AIRFLOW_CONTAINER_NAME airflow connections add 'my_prod_db' \
  --conn-type 'postgres' \
  --conn-host "${POSTGRES_HOST_CONN}" \
  --conn-schema "${POSTGRES_DB}" \
  --conn-login "${POSTGRES_USER}" \
  --conn-password "${POSTGRES_PASSWORD}" \
  --conn-port "${POSTGRES_PORT}"
