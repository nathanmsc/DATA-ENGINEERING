#!/bin/bash

#download hive files
wget https://downloads.apache.org/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz
tar -vzxf apache-hive-3.1.2-bin.tar.gz

#move to opt
mv hive-3.1.2 /opt/hive

#install jdk 8
apt install openjdk-8-jdk


