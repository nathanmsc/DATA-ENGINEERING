#!/bin/bash

# Set environment variables
export AIRFLOW_HOME=/home/airflow/airflow
export PATH=$PATH:/home/airflow/.local/bin
export TZ=America/Region
export AIRFLOW_VERSION=2.10.0
export USERNAME=airflow

# Create and set up the working directory
mkdir -p $AIRFLOW_HOME
cd $AIRFLOW_HOME

# Install system dependencies
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    libpq-dev \
    libpq5 \
    sudo \
    curl \
    postgresql-client
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

# Create a default user and add to the sudo group
sudo adduser --disabled-password --gecos "" $USERNAME
sudo usermod -aG sudo $USERNAME
sudo chown -R $USERNAME:$USERNAME /home/airflow
echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers

# Switch to the new user (in the context of this script)
sudo su - $USERNAME << EOF

# Install Airflow using the constraints file
PYTHON_VERSION="\$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-\${AIRFLOW_VERSION}/constraints-\${PYTHON_VERSION}.txt"
pip install "apache-airflow==\${AIRFLOW_VERSION}" --constraint "\${CONSTRAINT_URL}"

# Install additional libraries for PostgreSQL
pip install psycopg2-binary apache-airflow-providers-common-sql apache-airflow-providers-postgres

# Download the airflow.cfg file if you have custom settings
curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/DOCKER/AIRFLOW/airflow.cfg

# Initialize the Airflow database
airflow db init

# Create an Airflow user
airflow users create \
    --username user \
    --password "user" \
    --firstname user \
    --lastname IT \
    --role Admin \
    --email nathan@mindsetcloud.net

# Start the Airflow webserver and scheduler
airflow webserver --port 8080 &
airflow scheduler

EOF
