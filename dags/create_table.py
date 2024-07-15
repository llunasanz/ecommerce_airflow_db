from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
from operators.PostgresFileOperator import PostgresFileOperator
import os
import subprocess

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define a logging function to log the task status
def log_status(**context):
    logging.info("Creating table in PostgreSQL")

# Function to run the fetch_data.py script
def fetch_and_write_data():
    subprocess.run(['python3', '/opt/airflow/dags/get_info_from_mercadolibre_api.py', '--category', 'MLA1577', '--output_file', '/opt/airflow/output.tsv'], check=True)

# Define the DAG
with DAG(
    dag_id="create_db_postgres",
    default_args=default_args,
    description='A simple DAG to create a table in PostgreSQL',
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    log_task = PythonOperator(
        task_id='log_status',
        python_callable=log_status,
    )

    create_table_task = PostgresOperator(
        task_id="create_table_postgres",
        postgres_conn_id="my_prod_db",
        sql="""
            CREATE TABLE IF NOT EXISTS mercadolibre_items (
                id VARCHAR(30),
                title VARCHAR(255),
                price VARCHAR(10),
                sold_quantity VARCHAR(20),
                thumbnail VARCHAR(255),
                created_date VARCHAR(32),
                PRIMARY KEY(id, created_date)
            )
        """
    )

    fetch_data_task = PythonOperator(
        task_id='fetch_and_write_data',
        python_callable=fetch_and_write_data,
    )

    insert_data_task = PostgresFileOperator(
        task_id="insert_data_postgres",
        operation="write",
        config={"table_name": "mercadolibre_items"}
    )

    log_task >> create_table_task >> fetch_data_task >> insert_data_task
