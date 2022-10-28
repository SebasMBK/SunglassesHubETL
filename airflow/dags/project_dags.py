from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

with DAG(
    'sunglasseshub_etl',
    start_date=datetime(2022,10,28),
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1
) as dag:

    hello_world = BashOperator(
        task_id="hello",
        bash_command="cat /opt/airflow/tasks/LoadDataSQL/parameters/database.ini"
        )

