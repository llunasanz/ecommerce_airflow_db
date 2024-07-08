# Setup
## Some commands extracted from documentation: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

up_airflow:
	docker compose up airflow-init
	docker compose up

up_airflow_detach:
	docker compose up -d airflow-init
	docker compose up -d

connect_airflow_to_db:
	bash ./src/connect_airflow_to_db.sh

wait_for_airflow:
	bash ./src/wait_for_airflow.sh

up_and_connect:
	make up_airflow_detach && make wait_for_airflow && make connect_airflow_to_db

down_airflow:
	docker compose down --volumes --remove-orphans
