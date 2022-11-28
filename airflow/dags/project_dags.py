from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import date

default_args = {"owner": "airflow"}
start = days_ago(2)

with DAG(
    'sunglasseshub_etl',
    start_date=start,
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=['Scraper']
) as dag:


    data_scraper = BashOperator(
        task_id="datascraper",
        bash_command="python /opt/airflow/tasks/DataScraper/main.py"
        )

    data_cleaning = BashOperator(
        task_id="data_cleaning",
        bash_command="python /opt/airflow/tasks/DataValidator/main.py"
        )

    load_to_sql = BashOperator(
        task_id="load_to_sql",
        bash_command="python /opt/airflow/tasks/LoadDataSQL/main.py",
        )
    
    data_scraper >> data_cleaning >> load_to_sql

