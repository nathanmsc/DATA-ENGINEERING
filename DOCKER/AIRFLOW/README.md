# AIRFLOW
## _Airflow_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://nodesource.com/products/nsolid)

### install on ubuntu:
[ _shell_ ](https://github.com/mindsetcloud/infra-data-engineer/blob/main/docker/airflow/install.sh) - shell

### install within docker compose:
[ _docker-compose_ ](https://github.com/mindsetcloud/infra-data-engineer/blob/main/docker/airflow/airflow.yml) - docker-compose

### _install within dockerfile:_
[ _dockerfile_ ](https://github.com/mindsetcloud/infra-data-engineer/blob/main/docker/airflow/Dockerfile) - dockerfile

### _docker run:_

```sh
docker run --user airflow -it -d --name airflow-server --hostname airflow-server --restart=always --net postgres_default --ip 192.168.32.22 -v ~/bigdata/data/airflow:/home/airflow/airflow -p 8282:8282 msc/airflow
```


