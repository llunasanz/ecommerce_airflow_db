from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
from operators.PostgresFileOperator import PostgresFileOperator
import os
import json
import csv

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

# Define a function to write JSON data to TSV
def write_json_to_tsv(json_data, tsv_file_path):
    os.makedirs(os.path.dirname(tsv_file_path), exist_ok=True)
    fieldnames = json_data[0].keys()
    with open(tsv_file_path, mode='w', newline='') as tsv_file:
        writer = csv.DictWriter(tsv_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for item in json_data:
            writer.writerow(item)

# Function to fetch data and write to TSV
def fetch_and_write_data(**context):
    category = 'MLA1577'  # Example category
    url = f"https://api.mercadolibre.com/sites/MLA/search?category={category}#json"
    response = requests.get(url).text
    response_json = json.loads(response)
    data = response_json["results"]

    # Define keys to extract and their default values
    keys_to_extract = {
        'id': None,
        'title': None,
        'price': 0,
        'sold_quantity': 0, 
        'thumbnail': None
    }

    # Create a list of new JSON objects with only the required fields
    new_json_list = [
        dict(map(lambda k: (k, item.get(k, keys_to_extract[k])), keys_to_extract.keys()))
        for item in data
    ]

    # Write the new JSON data to TSV
    write_json_to_tsv(new_json_list, '/opt/airflow/output.tsv')

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
                PRIMARY KEY(id)
            )
        """
    )

    #fetch_and_write_task = PythonOperator(
    #    task_id='fetch_and_write_data',
    #    python_callable=fetch_and_write_data,
    #    provide_context=True,
    #)

    insert_data_task = PostgresFileOperator(
        task_id="insert_data_postgres",
        operation="write",
        config={"table_name": "mercadolibre_items"}
    )

    log_task >> create_table_task >> insert_data_task
