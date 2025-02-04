
# Docker Installation Guide

This guide provides step-by-step instructions for installing Docker on Ubuntu and setting up Docker Compose.

---

## Installing Docker on Ubuntu

### Option 1: Install via Script

Use the following command to quickly install Docker using a script:

```sh
curl -fsSL https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/docker.sh | sh
```

---

### Option 2: Manual Installation

#### Step 1: Update System and Install Dependencies

Run these commands to update the system and install the necessary packages:

```sh
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    software-properties-common \
    apt-transport-https \
    lsb-release
```

#### Step 2: Add Docker's Official GPG Key

Create a directory for storing the GPG key and add Docker's official GPG key:

```sh
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

#### Step 3: Add Docker's Repository

Add the Docker repository to your system:

```sh
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update the package index:

```sh
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
```

#### Step 4: Install Docker

Run the following commands to install Docker and verify the installation:

```sh
apt-cache policy docker-ce
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#### Step 5: Add User to the Docker Group

To avoid using `sudo` with Docker commands, add your user to the Docker group:

```sh
sudo usermod -aG docker ${USER}
```

---

## Installing Docker Compose

Docker Compose allows you to define and manage multi-container Docker applications.

### Step 1: Download Docker Compose

Download the Docker Compose binary and make it executable:

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Verify the Installation

Check the version to confirm Docker Compose is installed:

```sh
docker-compose --version
```

---

## Additional Docker Commands

### Get Container ID

Retrieve the ID of a specific container:

```sh
docker inspect --format="{{.Id}}" container
```

### Edit Container Configuration

To modify the container's configuration, edit the container file by its ID:

```sh
vim /var/lib/docker/containers/<ID>
```

## Useful Commands

### Git Setup

```bash
ssh-keygen -t rsa -b 4096 -C "your@email.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
clip < ~/.ssh/id_rsa.pub
# Add the key to GitHub
git pull git@github.com:username/repository.git
git config --global user.email "your@email.com"
git config --global user.name "your_name"
git push --set-upstream origin master
```

---

## Network Configuration

### Show IP Address of Interfaces

```bash
ip addr
```

### Create Macvlan Network with Docker

```bash
docker network create -d macvlan \
  --subnet=172.27.136.42/20 \
  --ip-range=172.27.142.0/24 \
  --gateway=172.27.128.1 \
  --aux-address="msc-router=172.27.142.1" \
  -o parent=eth0 msc-macvlan
```

### Link Macvlan Interface

```bash
sudo ip link add msc-macvlan link eth0 type macvlan mode bridge
sudo ip addr add 172.27.142.1/24 dev msc-macvlan
sudo ifconfig msc-macvlan up
```

### Create Bridge Network in Docker

```bash
docker network create \
  --driver=bridge \
  --subnet=192.168.32.0/16 \
  --ip-range=192.168.32.0/24 \
  --gateway=192.168.32.1 mindsetcloud-nt
```

#### Example of Custom Network:

```bash
docker network create \
  --subnet=10.10.1.0/24 \
  --ip-range=10.10.1.128/25 \
  --gateway=10.10.1.129 my_custom_network

# Verify the created network:
docker network inspect my_custom_network

# Run a container with a fixed IP:
docker run -d --name my_container \
  --net my_custom_network \
  --ip 10.10.1.130 image_name
```

Reference: [Docker Labs - Macvlan](https://dockerlabs.collabnix.com/beginners/macvlan-010.html)

---

## Running Docker on WSL

### WSL Installation and Setup

```bash
wsl --install
wsl --set-default-version 2
wsl --list --verbose
wsl --unregister <DistributionName>
wsl --list --online
wsl --install <DistributionName>
```

### Network Configuration in Windows

```bash
netsh interface ipv4 set address name="Ethernet" static 192.168.1.10 255.255.255.0 192.168.1.1
netsh interface ipv4 set dnsservers name="Ethernet" static 8.8.8.8 primary
netsh interface ipv4 add dnsservers name="Ethernet" 8.8.4.4 index=2
netsh interface portproxy add v4tov4 listenport=port listenaddress=0.0.0.0 connectport=port connectaddress=wsl_ip
```

---

## Service Permissions on Linux

Add the following lines to the `/etc/sudoers` file or use `visudo`:

```bash
username ALL=NOPASSWD: /usr/sbin/service ssh start
username ALL=NOPASSWD: /usr/sbin/service docker start
```

---

### Configuration in `~/.bashrc`

Add the following commands to the profile file:

```bash
vim ~/.bashrc
sudo service ssh start
sudo service docker start
```
