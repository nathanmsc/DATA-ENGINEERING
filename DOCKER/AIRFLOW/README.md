# AIRFLOW
## _Airflow_

# Project Overview

This project involves setting up and configuring Apache Airflow, a platform to programmatically author, schedule, and monitor workflows. Below, you'll find descriptions of the various files used in this project, along with links to the corresponding scripts.

## Files and Code Context

### 1. [Bash Script](link-to-bash-file)
The Bash script is designed to automate the installation and configuration of Apache Airflow on a Unix-based system. It handles tasks such as setting up environment variables, installing system dependencies, creating a default user, and initializing the Airflow database. This script is ideal for environments where Docker or Kubernetes is not available, and you need to set up Airflow directly on the host machine.

### 2. [Dockerfile](link-to-dockerfile)
The Dockerfile defines a containerized environment for Apache Airflow. It sets up the necessary environment variables, installs dependencies, creates a user, and configures Airflow with PostgreSQL support. This Dockerfile is useful when you want to deploy Airflow in a containerized environment, ensuring consistency and ease of deployment across different environments.

### 3. [Kubernetes YAML Manifest](link-to-yaml-file)
The Kubernetes YAML manifest describes the deployment of the Airflow server within a Kubernetes cluster. It specifies the container image, environment variables, ports, and other configurations needed to run Airflow on Kubernetes. This file is useful for orchestrating the deployment of Airflow in a scalable and resilient manner using Kubernetes.

## Usage

- **Bash Script:** Use the Bash script when you need to set up Airflow on a local or remote server without using Docker or Kubernetes.
- **Dockerfile:** Use the Dockerfile to build a Docker image for Airflow, which can then be deployed on any Docker-compatible platform.
- **Kubernetes YAML Manifest:** Use the Kubernetes YAML manifest to deploy Airflow on a Kubernetes cluster.

## Links

- [Bash Script](link-to-bash-file)
- [Dockerfile](link-to-dockerfile)
- [Kubernetes YAML Manifest](link-to-yaml-file)

---

For more details on how to use these files, refer to the official [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/).



### _docker run:_

```sh
docker run --user airflow -it -d --name airflow-server --hostname airflow-server --restart=always --net postgres_default --ip 192.168.32.22 -v ~/bigdata/data/airflow:/home/airflow/airflow -p 8282:8282 msc/airflow
```


