#!/bin/bash
apt install openjdk-8-jdk

tar xvzf streamsets-datacollector-common-3.22.3.tgz

cd streamsets-datacollector-3.22.3

vim ~/.profile

export PATH=$PATH:/lib/jvm/java-8-openjdk-arm64/bin:/opt/streamsets/bin

source ~/.profile

ulimit -n 32800

streamsets dc

 /opt/streamsets/bin/streamsets dc

localhost:18630

https://accounts.streamsets.com/install/instruction/data-collector/linux/common-tarball

https://accounts.streamsets.com/install/instruction/transformer-etl/linux/full-tarball

