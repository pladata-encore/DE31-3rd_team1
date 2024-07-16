# Base image with Python 3.10 and Airflow
FROM apache/airflow:2.9.2-python3.10

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Install OS dependencies
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    libmysqlclient-dev \
    autoconf \
    automake \
    libtool \
    pkg-config \
    perl \
    && apt-get clean

# Install specific version of automake
RUN wget http://ftp.gnu.org/gnu/automake/automake-1.11.tar.gz && \
    tar -xzf automake-1.11.tar.gz && \
    cd automake-1.11 && \
    ./configure && \
    make && \
    make install && \
    cd ..

# Install MeCab
RUN wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz && \
    tar xvfz mecab-0.996-ko-0.9.2.tar.gz && \
    cd mecab-0.996-ko-0.9.2 && \
    ./configure && \
    make && \
    make check && \
    make install && \
    ldconfig && \
    cd ..

# Install MeCab dictionary
RUN wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz && \
    tar xvfz mecab-ko-dic-2.1.1-20180720.tar.gz && \
    cd mecab-ko-dic-2.1.1-20180720 && \
    ./configure && \
    make && \
    make install && \
    cd ..

# Create Airflow logs directory and set permissions
RUN mkdir -p /opt/airflow/logs/dag_processor_manager && \
    chown -R airflow: /opt/airflow

# Install Python dependencies
USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install MeCab for KoNLPy
RUN bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)

# Copy the Airflow configuration file
USER root
COPY airflow.cfg $AIRFLOW_HOME/airflow.cfg

# Copy the dags and modules folders
COPY dags/ $AIRFLOW_HOME/dags
COPY modules/ $AIRFLOW_HOME/modules/

# Copy the init script and set permissions
COPY init_airflow.sh /init_airflow.sh
RUN chmod +x /init_airflow.sh

# Set entrypoint
USER airflow
ENTRYPOINT ["/init_airflow.sh"]

# Expose the port
EXPOSE 23044
