#!/bin/bash

# Define the Airflow webserver container name
AIRFLOW_CONTAINER_NAME="ecommerce_airflow_db-airflow-webserver-1"
AIRFLOW_HEALTH_URL="http://localhost:8080/health"

# Function to check if Airflow is up
is_airflow_up() {
    local response=$(docker exec $AIRFLOW_CONTAINER_NAME curl -s "$AIRFLOW_HEALTH_URL")
    echo "Response from Airflow health endpoint: $response"
    
    local metadatabase_status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['metadatabase']['status'])")
    local scheduler_status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['scheduler']['status'])")

    echo "Metadatabase status: $metadatabase_status"
    echo "Scheduler status: $scheduler_status"

    [ "$metadatabase_status" == "healthy" ] && [ "$scheduler_status" == "healthy" ]
}

# Wait until Airflow is up
echo "Waiting for Airflow to be up and running..."
while ! is_airflow_up; do
    echo "Airflow is not ready yet. Waiting..."
    sleep 5
done

echo "Airflow is up and running."

