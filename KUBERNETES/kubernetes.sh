#!/bin/bash

# Clear the terminal screen
clear

# Update system packages
echo "UPDATING PACKAGES"
echo "Reference: https://www.youtube.com/watch?v=o6bxo0Oeg6o"
sudo apt update -y
sleep 2

# Clear the terminal screen
clear

# Install Docker (assuming docker.sh is a script for installation)
echo "INSTALLING DOCKER"
echo "Running: ./docker.sh"
curl -fsSL https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/docker.sh | sh
sleep 2

# Clear the terminal screen
clear

# Install Git
echo "INSTALLING GIT"
sudo apt install git-all -y
sleep 2

# Clear the terminal screen
clear

# Install Go language
echo "INSTALLING GO LANGUAGE"
echo "Running: ./go.sh"
curl -fsSL https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/go.sh | sh
sleep 2

# Clear the terminal screen
clear

# Install CRI-Docker
echo "INSTALLING CRI-DOCKER"
echo "Reference: https://github.com/Mirantis/cri-dockerd"
git clone https://github.com/Mirantis/cri-dockerd.git
sudo mv cri-dockerd /opt
sudo chown -R ${USER}:${USER} /opt/cri-dockerd
sudo mkdir /opt/cri-dockerd/bin
cd /opt/cri-dockerd && sudo go build -o bin/cri-dockerd
sudo mkdir -p /usr/local/bin
sudo install -o root -g root -m 0755 /opt/cri-dockerd/bin/cri-dockerd /usr/local/bin/cri-dockerd
sudo cp -a packaging/systemd/* /etc/systemd/system
sudo sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' /etc/systemd/system/cri-docker.service
sleep 2

# Clear the terminal screen
clear

# Reload system daemon and enable CRI-Docker services
echo "RELOADING SYSTEM DAEMON"
sudo systemctl daemon-reload
sudo systemctl enable cri-docker.service
sudo systemctl enable --now cri-docker.socket
sleep 2

# Clear the terminal screen
clear

# Add Kubernetes APT repository
echo "ADDING KUBERNETES APT REPOSITORY"
echo "Reference: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/"
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sleep 2

# Clear the terminal screen
clear


# Install Kubernetes components
echo "INSTALLING KUBEADM AND KUBECTL"
sudo swapoff -a; sed -i '/swap/d' /etc/fstab
cat >> /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysclt --system
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet
sleep 2

# Clear the terminal screen
clear
