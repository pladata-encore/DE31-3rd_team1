from datetime import datetime
import pandas as pd
import json
import os
from urllib import parse
import subprocess
from hdfs import InsecureClient
from tqdm import tqdm
from konlpy.tag import Mecab
from collections import Counter
import pymysql
import time


def main():
    mecab = Mecab()
    today = datetime.today().strftime("%Y-%m-%d")
    client_hdfs = InsecureClient("http://192.168.0.206:50070")

    # HDFS 파일 읽기 함수
    def read_hdfs_file(client, path, max_retries=5, delay=5):
        retries = 0
        while retries < max_retries:
            try:
                with client.read(path) as reader:
                    return pd.read_csv(reader, encoding='utf-8')
            except Exception as e:
                print(f"Error reading file {path}: {e}")
                retries += 1
                if retries < max_retries:
                    print(f"Retrying... ({retries}/{max_retries})")
                    time.sleep(delay)
        raise Exception(f"Failed to read file {path} after {max_retries} attempts")

    # 뉴스 내용을 포함한 CSV 파일 읽기
    news_contents = read_hdfs_file(client_hdfs, f'/test/{today}.csv')
    news_contents = news_contents.dropna()

    tmp = []
    for content in news_contents['content']:
        word = mecab.nouns(content)
        tmp.extend(word)

    nouns = [t for t in tmp if len(t) > 1]

    df = pd.DataFrame.from_dict(Counter(nouns), orient='index').reset_index()
    df.columns = ['Keyword', 'count']
    df = df.sort_values(by='count', ascending=False).reset_index(drop=True)

    user = 'class5'
    password = '123'
    host = '43.202.5.70'
    port = 3306
    database = 'encore_web'
    password = parse.quote_plus(password)

    # pymysql을 사용하여 MySQL에 연결
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 테이블이 없으면 생성
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS `{today}` (
                `Keyword` VARCHAR(255) NOT NULL,
                `count` INT NOT NULL
            )
            """
            cursor.execute(create_table_query)
            
            # 데이터 삽입
            for index, row in df.iterrows():
                insert_query = f"""
                INSERT INTO `{today}` (`Keyword`, `count`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE `count` = VALUES(`count`)
                """
                cursor.execute(insert_query, (row['Keyword'], row['count']))
        
        connection.commit()
        print(f"Data successfully saved to table {today}.")
    except Exception as e:
        print(f'Error: {e}')
    finally:
        connection.close()

if __name__ == '__main__':
    main()