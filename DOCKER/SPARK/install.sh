apt install openjdk-8-jdk

export PATH=$PATH:/lib/jvm/java-8-openjdk-arm64/bin:/opt/streamsets/bin


docker run -it -d --name spark-master --hostname spark-master --restart=always --net mindsetcloud-nt --ip 192.168.32.24 -p 8080:8080 -p 4040:4040 mindsetcloud/spark-cluster:arm64
docker run -it -d name spark-worker-01 hostname spark-worker-01 --restart=always --net mindsetcloud-nt --ip 192.168.32.25 mindsetcloud/spark-cluster:arm64
docker run -it -d name spark-worker-02 hostname spark-worker-02  --restart=always --net mindsetcloud-nt --ip 192.168.32.26 mindsetcloud/spark-cluster:arm64


vim hosts

192.168.32.24 spark-master
192.168.32.25 spark-worker-01
192.168.32.26 spark-worket-02

apt install openss-server openssh-clients openssh-libs
ssh-keygen -t rsa -P ""
cat id_rsa.pub > authorized_keys
copiar authorized_keys para as demais do cluster

600
700

donload apacche-spark

wget https://www.apache.org/dyn/closer.lua/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz

vim .profile
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin

source .profile

cd /opt/spark/conf

cp spark-env.sh.template spark-env.sh
cp slaves.template slaves

vim slaves
spark-worker-01
spark-worker-02

vim spark-env.sh
export SPARK_MASTER_HOST=192.168.32.24
export JAVA_HOME=/lib/jvm/java-8-openjdk-arm64/

sbin/ ./start-all.sh

jps

pyspark








