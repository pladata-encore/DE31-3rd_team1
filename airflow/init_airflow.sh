#!/bin/bash
airflow db init
airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com --password admin
airflow standalone

