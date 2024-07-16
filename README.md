
# DE31-3rd&4th_team2

# 경제 기사 키워드 분석 프로젝트

## 프로젝트 개요
이 프로젝트는 네이버 경제 기사를 크롤링하고, 바른API를 이용해 키워드를 추출하여, Apache Airflow를 통해 데이터 파이프라인을 관리합니다. 데이터를 Hadoop HDFS에 저장하고, Apache Spark를 이용해 전처리한 후, MYSQL에 저장합니다. Django를 이용해 웹 서버를 구축하고, DB에서 전처리한 파일들을 불러와 워드클라우드와 바 차트를 시각화합니다.

## 팀 구성
- 기석광: 데이터 크롤링 및 데이터 파이프라인 관리, docker airflow 구축
- 최태성: 키워드 추출 및 데이터 저장
- 조명아: Hadoop 구축 및 Spark 구축
- 차민혁: Django 구축 및 시각화, docker 환경 구축, 스프링부트 API 구축
- 신소영: Django 구축 및 시각화, docker 환경 구축

## 프로젝트 구조
1. 데이터 수집 및 비동기 크롤링
2. 전처리 통한 키워드 추출
3. 데이터 워크플로우 관리
4. 데이터 저장
5. 데이터 시각화
```
DE31-3rd_team2
├── airflow
│   ├── airflow.cfg              # Airflow 설정 파일
│   ├── dags                     # DAG 정의 파일들이 있는 디렉토리
│   │   └── news_crawling_dag.py
│   ├── docker-compose.yml       # Airflow를 위한 Docker Compose 설정 파일
│   ├── Dockerfile               # Airflow 이미지를 빌드하기 위한 Dockerfile
│   ├── init_airflow.sh          # Airflow 초기화를 위한 스크립트
│   ├── logs                     # Airflow 로그 디렉토리
│   │   └── scheduler            # 스케줄러 관련 로그
│   ├── modules                  # Airflow 태스크를 위한 커스텀 파이썬 모듈들
│   │   ├── keyword_ext_mecab.py
│   │   ├── keyword_ext.py
│   │   └── news_crawling.py
│   └── requirements.txt         # Airflow를 위한 파이썬 의존성 파일
└── django
    └── web
        ├── chart                # 차트 기능을 위한 Django 앱
        │   ├── admin.py
        │   ├── models.py
        │   ├── views.py
        │   ├── urls.py
        ├── config               # Django 프로젝트 설정
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        ├── docker-compose.yml   # Django를 위한 Docker Compose 설정 파일
        ├── Dockerfile           # Django 이미지를 빌드하기 위한 Dockerfile
        ├── manage.py            # Django 관리 스크립트
        ├── requirements.txt     # Django를 위한 파이썬 의존성 파일
        ├── static               # 정적 파일들 (CSS, JavaScript, 이미지 등)
        │   ├── bootstrap.min.css
        │   ├── bootstrap.min.js
        │   └── style.css
        └── templates            # HTML 템플릿들
            ├── base.html
            ├── chart.html
            ├── index.html
            └── navbar.html
```

## 기술 스택
- **Python**: 데이터 수집 및 크롤링, 키워드 추출
- **Asyncio**, **BeautifulSoup**, **Requests**: 크롤링
- **바른API**: 키워드 추출
- **Apache Airflow**: 데이터 파이프라인 관리
- **Apache Hadoop (HDFS)**: 데이터 저장
- **Apache Spark**: 데이터 전처리
- **MySQL**: 데이터 저장
- **django**: python 기반 웹 페이지 구현
- **docker**: 컨테이너 환경에서 airflow, django 를 실행하기 위해 사용
- **JavaScript (Chart.js)**: 데이터 시각화
- **HTML/CSS**: 웹 페이지 구성
- **Spring Boot**: API 서버 구축




## 단계별 작업

### 1. 데이터 수집 및 비동기 크롤링
- **담당자**: 기석광, 조명아
- **과정**:
  1. nest_asyncio 모듈을 이용하여 비동기 방식으로 네이버 경제 기사를 크롤링한다. 
  2. 추출된 데이터를 구조화된 형식으로 HDFS에 csv파일로 전송한다.
- 자세한 코드는 [여기](https://github.com/pladata-encore/DE31-3rd_team2/blob/seokkwang/modules/news_crawling.py)를 참고

### 2-1. 데이터 전처리(바른API)
- **담당자**: 조명아, 최태성
- **과정**:
	1. HDFS에 저장된 데이터를 Spark를 이용해 로드
  2. 기사 내용 데이터를 바른API에 요청하여 키워드 추출
  3. 키워드와 해당 키워드의 빈도수를 집계하여 DB에 저장할 형식으로 변환
- 자세한 코드는 [여기](https://github.com/pladata-encore/DE31-3rd_team2/blob/develop/airflow/modules/keyword_ext.py)를 참고

### 2-2. 데이터 전처리(Mecab)
- **담당자**: 조명아, 최태성
- **과정**:
	1. HDFS에 저장된 데이터를 로드
  2. 기사 내용 데이터를 Mecab 모듈의 형태소 분석을 통해 키워드 추출
  3. 키워드와 해당 키워드의 빈도수를 집계하여 DB에 저장할 형식으로 변환
- 자세한 코드는 [여기](https://github.com/pladata-encore/DE31-3rd_team2/blob/develop/airflow/modules/keyword_ext_mecab.py)를 참고

### 3. 데이터 워크플로우 관리
- **담당자**: 기석광, 최태성
- **과정**:
  1. Airflow DAG을 정의하여 크롤링, 데이터 저장 및 전처리 작업을 자동화
  2. 각각의 작업(Task)을 단계별로 정의하고 의존성 설정
- 자세한 코드는 [여기](https://github.com/pladata-encore/DE31-3rd_team2/blob/develop/airflow/dags/news_crawling_dag.py)를 참고
  

### 4. django 웹페이지 제작 및 데이터 시각화
- **담당자**: 신소영, 차민혁
- **과정**:
  1. Django 템플릿을 이용해 기본 웹 페이지 구성
  2. 날짜 입력 폼을 제공하여 원하는 날짜 입력
  3. 입력된 날짜에 해당하는 키워드 데이터를 mysql에서 조회
  4. 조회된 데이터를 바탕으로 python 라이브러리를 이용해 워드클라우드로 구현하고 chart.js 를 활용해 차트 생성 
 
### 5. docker 실행 환경 구축
- **담당자**: 신소영, 차민혁
- **과정**:
  1. dockerfile , docker-compose.yml 파일 제작
  2. 도커환경에서 애플리케이션을 실행 할 수 있도록 환경 구축
 

### 6. API 서버 구축
- **담당자**: 차민혁
- **과정**:
  1. 스프링 부트 애플리케이션을 설정하고,  API 문서화 설정
  2. 엔티티와 레포지토리를 구현하여 CRUD API를 제작
  3. 키워드 카운트 서비스 및 콘트롤러 구현하여 비즈니스 로직 처리
  4. 동적 엔티티 및 콘트롤러 통해 동적 테이블 조회 
  
## 하둡 및 스파크 클러스터 설정

#### 하둡 설정 파일 수정

- `core-site.xml`:
- `hdfs-site.xml`:
- `mapred-site.xml`:
- `yarn-site.xml`:
- `workers`:
``` bash
    datanode1
    datanode2
```
#### 하둡 클러스터 시작
``` bash
    ssh namenode start-dfs.sh
    ssh secondnode start-yarn.sh
	ssh namenode mr-jobhistory-daemon.sh start historyserver
```
#### 스파크 설정 파일 수정
- `spark-env.sh`
```bash
export SPARK_MASTER_HOST='master' 
export SPARK_WORKER_CORES=4 
export SPARK_WORKER_MEMORY=4g
```
- `workers`:
``` bash
    worker1
    worker2
```
#### 스파크 클러스터 시작 
```bash 
$SPARK_HOME/sbin/start-all.sh 
```
  

## 설치 및 실행 방법

### 요구 사항
- Python 3.10.14
- Apache Hadoop
- Apache Spark
- Apache Airflow
- MySQL 8.0.37
- Django 5.0.7
- docker 27.0.3
- spring boot 3.2.7

### 설치

1. **Python 패키지 설치**:
    ```bash
    pip install asyncio beautifulsoup4 requests Django psycopg2-binary
    ```

2. **Hadoop설치**:
	```bash
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
	tar xvzf ./hadoop-3.3.6.tar.gz
    ```
    
3. **Spark 설치**

```bash
wget https://dlcdn.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz
	tar xvzf ./spark-3.4.3-bin-hadoop3.tgz
```


4. **Airflow 설치**:
    ```bash
    pip install apache-airflow
    ```

5. **MYSQL 설치**:
  ```bash
	pip install mysqlclient
   ```

6. **docker 설치**:
   ```bash
    curl -sSL get.docker.com | sh
   ```  
    
    

### 실행

1. **데이터 크롤러 실행**:
    ```bash
    python crawler.py
    ```

2. **Airflow 시작**:
    ```bash
    airflow db init
    airflow webserver --port 8080
    airflow scheduler
    ```

3. **Django 서버 시작**:
    ```bash
    sudo service docker start
    docker compose up
    ```
    
    
  **django 웹페이지 기능 시연**
  
  
  
 ![Animation](https://github.com/user-attachments/assets/6c7f01ff-b297-480d-9552-969ff5b1fa8b)
     
     
  
  
  
  
     
  
4. **Spring Boot JAR 파일 실행**:
    ```bash
    java -jar target/advanced_jpa-0.0.1-SNAPSHOT.jar
    ```
  
  
![image](https://github.com/user-attachments/assets/964c902f-6631-40df-a411-bdcf7d39c5d9)
![image](https://github.com/user-attachments/assets/a066ad57-3bff-4fba-8389-eb524afced44)
![image](https://github.com/user-attachments/assets/b2ee3e7d-1de0-4ac6-a179-464e322b82db)
![image](https://github.com/user-attachments/assets/ee8298d7-4fc4-40d1-b962-715c114e2425)
  
  

  
  
