#!/bin/bash

# update packages
sudo apt update

# install java
sudo apt install default-jre

# download kafka 
wget https://downloads.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz

# move kafka to /opt
mv kafka /opt

# chance ownner 
sudo chown -R hadoop:hadoop /opt/kafka

# set file profile
vim .bash_profile

# add kafka variables on profile
export KAFKA_HOME=/opt/kafka
export PATH=$PATH:$KAFKA_HOME/bin

# apply settings
source .bash_profile

# init zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# init kafka
bin/kafka-server-start.sh config/server.properties

# create topic
bin/kafka-topics.sh --create --topic topic1 --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

# producer
bin/kafka-console-producer.sh --topic topic1 --bootstrap-server localhost:9092

# consumer
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic1 --from-beginning

