# Setup
## Commands extracted from documentation: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
up_airflow:
	docker compose up airflow-init

down_airflow:
	docker compose down --volumes --remove-orphans
