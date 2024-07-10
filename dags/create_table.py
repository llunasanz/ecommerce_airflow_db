from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
import os

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
        provide_context=True,
    )

    create_table_task = PostgresOperator(
        task_id="crear_tabla_postgres",
        postgres_conn_id="my_prod_db",
        sql="""
            CREATE TABLE IF NOT EXISTS mercadolibre_items (
                id VARCHAR(30),
                site_id VARCHAR(30),
                title VARCHAR(50),
                price VARCHAR(10),
                sold_quantity VARCHAR(20),
                created_date VARCHAR(8),
                PRIMARY KEY(id, created_date)
            )
        """
    )

    log_task >> create_table_task
