from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
import os
import logging

class PostgresFileOperator(BaseOperator):

    @apply_defaults
    def __init__(self, operation, config={}, *args, **kwargs):
        super(PostgresFileOperator, self).__init__(*args, **kwargs)
        self.operation = operation
        self.config = config

        # Load environment variables from the .env file
        self.load_env_file('/opt/airflow/config/.env')
        
        self.postgres_hook = PostgresHook(postgres_conn_id='my_prod_db')

    def execute(self, context):
        if self.operation == "write":
            self.write_in_postgres_table()
        elif self.operation == "read":
            pass
        else:
            pass

    def write_in_postgres_table(self):
        table_name = self.config.get('table_name')
        file_path = '/opt/airflow/output.tsv'

        logging.info(f"Starting bulk load into table {table_name} from file {file_path}")
        
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} does not exist.")
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        # Assuming the file is tab-separated, bulk load the data
        try:
            self.postgres_hook.bulk_load(table_name, file_path)
            logging.info(f"Bulk load into table {table_name} completed successfully.")
        except Exception as e:
            logging.error(f"Bulk load failed: {str(e)}")
            raise

    def load_env_file(self, filepath):
        with open(filepath) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
