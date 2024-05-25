import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.wikipedia_pipeline import extract_wikipedia_data
from datetime import datetime
dag = DAG(
    dag_id="Wikipedia_flow",
    default_args={
        "owner": "Sivaram Thampi",
        "start_date": datetime(2024, 5, 24)
    },
    schedule_interval=None,
    catchup=True 
)
extract_data_from_wikipedia = PythonOperator(
    task_id="extract_data_from_wikipedia",
    python_callable=extract_wikipedia_data,
    provide_context=True,
    op_kwargs={
        "url": "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
    },
    dag=dag
)
extract_data_from_wikipedia