# DATA-ENGINEERING
### DATA ENGINEERING TOOLS AND INFRAESTRUCTURE

By leveraging Kubernetes and containerization, organizations can build a resilient, scalable, and secure infrastructure for data engineering. This setup not only enhances the efficiency of data processing and analysis but also ensures that the infrastructure can adapt to evolving data challenges, providing a robust foundation for data-driven decision-making.

## Guide

- [Kubernetes](https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/KUBERNETES/README.md)
- [Docker Containers](https://github.com/nathanmsc/DATA-ENGINEERING/tree/main/DOCKER)
- [Contributing](#contributing)
- [License](#license)

### Utils Commands

Instructions on how to install and set up your project.

Git setup
```
ssh-keygen -t rsa -b 4096 -C "name@dominio.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
clip < ~/.ssh/id_rsa.pub
make ssh key on github
git pull git@github.com:user/repository.git
git config --global user.email "name@dominio.com"
git config --global user.name "name"
git push --set-upstream origin master
```

NETWORK

### show ip address interfaces
```sh

ip addr

```
### create network macvlan with docker
```sh
docker network create -d macvlan \
  --subnet=172.27.136.42/20 \
  --ip-range=172.27.142.0/24 \
  --gateway=172.27.128.1 \
  --aux-address="msc-router=172.27.142.1" \
  -o parent=eth0 msc-macvlan

```
### link macvlan interface
```sh
sudo ip link add msc-macvlan link eth0 type macvlan mode bridge
sudo ip addr add 172.27.142.1/24 dev msc-macvlan
sudo ifconfig msc-macvlan up
```

```
docker network create --driver=bridge --subnet=192.168.32.0/16 --ip-range=192.168.32.0/24 --gateway=192.168.32.1 mindsetcloud-nt
```

```bash
#Criar a Rede Docker com a Sub-rede Específica:
#Utilize o comando docker network create para criar uma rede Docker com o intervalo de IPs desejado:

docker network create \
--subnet=10.10.1.0/24 \
--ip-range=10.10.1.128/25 \
--gateway=10.10.1.129 \
minha_rede_customizada

#--subnet=10.10.1.0/24: Define a sub-rede como 10.10.1.0/24, abrangendo todos os IPs de 10.10.1.1 a 10.10.1.254.
#--ip-range=10.10.1.128/25: Define o intervalo de IPs utilizável para os containers. Nesse caso, o intervalo vai de 10.10.1.128 até 10.10.1.254.
#--gateway=10.10.1.129: Especifica o IP do gateway da rede Docker. Você pode escolher qualquer IP dentro do intervalo, mas ele geralmente é o primeiro IP do intervalo definido.

#Verifique a Rede Criada:
#Após criar a rede, você pode verificar se foi criada corretamente usando o comando:

docker network inspect minha_rede_customizada

#Agora, você pode iniciar containers utilizando a rede criada e, se necessário, atribuir um IP específico dentro do intervalo:

docker run -d --name meu_container --net minha_rede_customizada --ip 10.10.1.130 <nome_da_imagem>
#Neste exemplo, o container meu_container será executado na rede minha_rede_customizada com o IP 10.10.1.130.
```
reference: https://dockerlabs.collabnix.com/beginners/macvlan-010.html

Running Docker on WSL

```bash
wsl --list --verbose
wsl --unregister <DistributionName>
wsl --list --online
wsl --install <DistributionName>
```

### Add the following lines to your /etc/sudoers file or visudo:
```sh
username ALL=NOPASSWD: /usr/sbin/service ssh start
username ALL=NOPASSWD: /usr/sbin/service docker start

```
### On profile file ~/.bashrc add the following:

```sh
vim ~/.bashrc
sudo service ssh start
sudo service docker start
```
