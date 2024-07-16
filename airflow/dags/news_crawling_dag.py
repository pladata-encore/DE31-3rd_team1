# dags/news_crawling_dag.py

from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
import sys
import os

# 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

# news_crawling 모듈 임포트
from news_crawling import scrape_news, transfer_to_hdfs
import keyword_ext_mecab 

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
    schedule_interval='30 22 * * *',  # 매일 밤 23:00에 실행
    catchup=False,
)


def scrape_news_task(**context):
    json_data = scrape_news()
    context['task_instance'].xcom_push(key='news_data', value=json_data)

def transfer_to_hdfs_task(**context):
    json_data = context['task_instance'].xcom_pull(key='news_data', task_ids='scrape_news')
    transfer_to_hdfs(json_data)

def keyword_ext_mecab_task():
    keyword_ext_mecab.main()

# 뉴스 크롤링 태스크
t1 = PythonOperator(
    task_id='scrape_news',
    python_callable=scrape_news_task,
    provide_context=True,
    dag=dag,
)

# HDFS 전송 태스크
t2 = PythonOperator(
    task_id='transfer_to_hdfs',
    python_callable=transfer_to_hdfs_task,
    provide_context=True,
    dag=dag,
)

t3 = PythonOperator(
    task_id='keyword_ext_mecab',
    python_callable=keyword_ext_mecab_task,
    provide_context=True,
    dag=dag,
)

t1 >> t2 >> t3