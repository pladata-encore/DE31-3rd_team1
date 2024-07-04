# dags/news_crawling_dag.py

from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys
import os
# spark submit operator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
# 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

# news_crawling 모듈 임포트
from news_crawling import scrape_news, transfer_to_hdfs
# from keyword_ext 
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

# SparkSubmitOperator를 사용하여 PySpark 작업을 제출
# spark_task = SparkSubmitOperator(
#     task_id='extract_keywords',
#     application='/home/ksk/project/third_project/modules/keyword_ext.py',  # your_spark_script.py 경로를 지정하세요.
#     conn_id='spark_default',
#     conf={
#         'spark.executor.instances': '2',
#         'spark.app.name': 'KeywordExtraction',
#     },
#     dag=dag,
# )

t1 >> t2
# spark_task