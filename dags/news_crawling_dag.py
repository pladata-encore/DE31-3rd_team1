# dags/news_crawling_dag.py

from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys
import os

# 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

# news_crawling 모듈 임포트
from news_crawling import scrape_news

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 30),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='news_crawling',
    description="Daily news crawling",
    default_args=default_args,
    schedule_interval='30 23 * * *',  # 매일 밤 23:30에 실행
    catchup=False,
)

t1 = PythonOperator(
    task_id='scrape_news',
    python_callable=scrape_news,
    dag=dag,
)
