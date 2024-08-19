#!/bin/bash

# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
export AIRFLOW_HOME=~/airflow
export PATH=$PATH:/home/airflow/.local/bin
export TZ=America/Region

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.5.1
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.7.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"



#install library postgres to connect on sqlalchemy
pip install psycopg2-binary
pip install apache-airflow-providers-common-sql
pip install psycopg2
pip install apache-airflow-providers-postgres
apt install libpq-dev
apt install libpq5

#edit file airflow.cfg
sql_alchemy_conn = postgresql://airflow:airflow@localhost/airflow

#create database and database user
psql -U postgres
postgres=# CREATE USER airflow PASSWORD 'airflow';
postgres=# CREATE DATABASE airflow;
postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;

#init database
airflow db init

#
# The Standalone command will initialise the database, make a user,
# and start all components for you.
airflow standalone

airflow users create --username user --password ********* --firstname user --lastname IT --role Admin --email user@domain

docker run -it -d --name airflow-server --hostname airflow-server --user airflow --restart=always --net mindsetcloud-nt --ip 192.168.32.4 -v ~/bigdata/data/airflow:/mnt/sources -p 8282:8282 -e AIRFLOW_HOME=/home/airflow/airflow -e TZ=America/Bahia mindsetcloud/airflow-postgres:arm64

# Visit localhost:8080 in the browser and use the admin account details
# shown on the terminal to login.
# Enable the example_bash_operator dag in the home page
