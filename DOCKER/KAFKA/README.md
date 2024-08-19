# KAFKA
## _Kafka broker and zookeeper_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://nodesource.com/products/nsolid)

### install on ubuntu:
[ _shell_ ](https://github.com/mindsetcloud/infra-data-engineer/blob/main/docker/kafka/install.sh) - shell

### install within docker compose:
[ _docker-compose_ ](https://github.com/mindsetcloud/infra-data-engineer/blob/main/docker/kafka/kafka.yml) - docker-compose

### _install within dockerfile:_
[ _dockerfile_ ](https://github.com/mindsetcloud/infra-data-engineer/blob/main/docker/kafka/Dockerfile) - dockerfile

## _kafka single cluster_

### init zookeeper
```sh
bin/zookeeper-server-start.sh config/zookeeper.properties
#run on background
nohup bin/zookeeper-server-start.sh config/zookeeper.properties >zookeeper.log &
```

### init kafka
```sh
bin/kafka-server-start.sh config/server.properties
```

### create topic
```sh
bin/kafka-topics.sh --create --topic topic1 --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
```

### producer
```sh
bin/kafka-console-producer.sh --topic topic1 --bootstrap-server localhost:9092
```

### consumer
```sh
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic1 --from-beginning
```

## _kafka multi cluster_

``` sh
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### create n files server_n(s).properties
```sh
cp config/server.properties conf/server_n.properties
```

### init kafka
```sh
bin/kafka-server-start.sh config/server.properties
bin/kafka-server-start.sh config/server_n.properties
```

### create topic
```sh
bin/kafka-topics.sh --create --topic topic1 --bootstrap-server localhost:9092 --replication-factor n --partitions 1
```

### producer
```sh
bin/kafka-console-producer.sh --topic topic1 --bootstrap-server localhost:9092
```

### references:
[ _documentation_ ](https://developer.confluent.io/quickstart/kafka-docker/) - kafka

