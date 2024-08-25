# Base image
FROM python:3.10-slim-buster

# Set environment variables
ENV AIRFLOW_HOME=/home/airflow/airflow
ENV PATH=$PATH:/home/airflow/.local/bin
ENV TZ=America/Region
ENV AIRFLOW_VERSION=2.10.0

# Set up working directory
WORKDIR $AIRFLOW_HOME

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    libpq5 \
    sudo \
    curl \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a default user and add to sudo group
ENV USERNAME=airflow

RUN adduser --disabled-password --gecos "" $USERNAME && \
    usermod -aG sudo $USERNAME && \
    chown -R $USERNAME:$USERNAME /home/airflow && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to the new user
USER $USERNAME

# Install Airflow using the constraints file
RUN PYTHON_VERSION="$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)" && \
    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" && \
    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Install additional libraries for PostgreSQL
RUN pip install psycopg2-binary apache-airflow-providers-common-sql apache-airflow-providers-postgres

# Expose necessary ports (if you intend to access Airflow's web UI)
EXPOSE 8080

# Copy the airflow.cfg (if you have custom settings)
RUN curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/DOCKER/AIRFLOW/airflow.cfg

# Initialize the Airflow database
RUN airflow db init

# Create Airflow user (for example purposes, use environment variables to pass secure values)
RUN airflow users create \
    --username user \
    --password "user" \
    --firstname user \
    --lastname IT \
    --role Admin \
    --email nathan@mindsetcloud.net

# Command to start Airflow
RUN airflow webserver --port 8080 &
CMD ["airflow", "scheduler"]
