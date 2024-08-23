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
curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/docker.sh
sudo chmod +x docker.sh
# Uncomment the next line to run the docker.sh script
./docker.sh
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
curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/go.sh
sudo chmod +x go.sh
./go
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
sudo swapoff -a
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet
sleep 2

# Clear the terminal screen
clear

# Get the IP address and configure the Pod network
IP_ADDRESS=$(ip addr show | grep 'inet' | awk '{print $2}' | grep -v -e '::' -e '127.0.0.1' -e '10.255.255.254' -e '172.17.0.1')
ENDPOINT=$(ip addr show | grep 'inet' | awk '{print $2}' | grep -v -e '::' -e '127.0.0.1' -e '10.255.255.254' -e '172.17.0.1' | cut -d'/' -f1)
echo "CONFIGURING POD NETWORK WITH IP: $IP_ADDRESS"
sudo kubeadm init --control-plane-endpoint $ENDPOINT:6443 --pod-network-cidr=$IP_ADDRESS --cri-socket=unix:///var/run/cri-dockerd.sock --v=5  --ignore-preflight-errors=all

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
sleep 4

# Clear the terminal screen
clear

# Install and configure Calico for networking
echo "INSTALLING AND CONFIGURING CALICO"
echo "Reference: https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises"
curl https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/calico.yaml -O
kubectl apply -f calico.yaml
sleep 2

# Clear the terminal screen
clear

# Validate Kubernetes installation
echo "VALIDATING KUBERNETES INSTALLATION"
kubectl get pods -A
echo "To join a node, use the following command:"
echo "kubeadm join <CONTROL_PLANE_IP>:6443 --token <TOKEN> \
        --discovery-token-ca-cert-hash sha256:<HASH> --cri-socket=unix:///var/run/cri-dockerd.sock"
