# DATA-ENGINEERING
### DATA ENGINEERING TOOLS AND INFRAESTRUCTURE


CONFIGURATION
```
ssh-keygen -t rsa -b 4096 -C "name@dominio.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
clip < ~/.ssh/id_rsa.pub
make ssh key on github
git pull git@github.com:elnataoliveira/mindsetcloud.git
git config --global user.email "name@dominio.comm"
git config --global user.name "namea"
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
reference: https://dockerlabs.collabnix.com/beginners/macvlan-010.html
