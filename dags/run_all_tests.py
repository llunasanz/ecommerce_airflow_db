from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'run_all_tests',
    default_args=default_args,
    description='A simple DAG to run all tests in the tests directory',
    schedule_interval=timedelta(days=1),
)

run_tests = BashOperator(
    task_id='run_tests',
    bash_command='python -m unittest discover -s /opt/airflow/tests',
    dag=dag,
)

