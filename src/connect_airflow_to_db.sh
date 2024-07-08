#!/bin/bash

# Load environment variables from the .env file
export $(grep -v '^#' .env | xargs)

# Get the PostgreSQL port number dynamically
POSTGRES_PORT=$(docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Ports}}" | awk '$2 ~ /postgres/ {split($3, a, ":"); split(a[2], b, "-"); print b[1]}')

# Construct the connection URI using the environment variables and the dynamically obtained port number
CONN_URI="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}"

# Define the Airflow webserver container name
AIRFLOW_CONTAINER_NAME="ecommerce_airflow_db-airflow-webserver-1"

# Add the connection to Airflow using Docker exec
docker exec -it $AIRFLOW_CONTAINER_NAME airflow connections add 'my_prod_db' --conn-uri "${CONN_URI}"

