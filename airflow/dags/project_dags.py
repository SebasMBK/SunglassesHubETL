from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonVirtualenvOperator

default_args = {"owner": "airflow"}

with DAG(
    'sunglasseshub_etl',
    start_date=datetime(2022,10,28),
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=['Scraper']
) as dag:


    data_scraper = BashOperator(
        task_id="datascraper",
        bash_command="python /opt/airflow/tasks/DataScraper/datascraper.py"
        )

    data_cleaning = BashOperator(
        task_id="data_cleaning_validator",
        bash_command="python /opt/airflow/tasks/DataValidator/data_cleaning.py"
        )

    load_to_sql = BashOperator(
        task_id="load_to_sql",
        bash_command="python /opt/airflow/tasks/LoadDataSQL/AzurePostgres.py",
        )
    
    data_scraper >> data_cleaning >> load_to_sql

