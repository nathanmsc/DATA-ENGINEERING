FROM ubuntu:latest

LABEL maintainer="mindsetcloud"

RUN apt-get update -y;

RUN apt install default-jre ; \
    apt install wget ; \
    wget https://downloads.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz ; \
    tar -vzxf kafka_2.13-3.3.1.tgz -C /opt/kafka 
       
ENV  KAFKA_HOME=/opt/kafka \
     PATH=${PATH}:${KAFKA_HOME}/bin
     
RUN /opt/kafka/bin/zookeeper-server-start.sh config/zookeeper.properties ; \
    /opt/kafka/bin/kafka-server-start.sh config/server.properties
