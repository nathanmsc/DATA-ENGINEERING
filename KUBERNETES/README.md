# KUBERNETES

# Kubernetes and Docker Setup Script

REQUIRE

```
#disable swap
#install docker
#insatall go 
```

This script automates the installation and configuration of Docker, CRI-Docker, Kubernetes, and other necessary tools on a Linux system.

[INSTALL KUBERNETES](https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/kubernetes.sh)

```bash
echo "INSTALLING KUBERNETES, DOCKER AND GOLANG"
```
```bash
curl -fsSL https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/kubernetes.sh | sh
```
or

```bash
echo "Running: ./kubernetes.sh"
curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/kubernetes.sh
sudo chmod +x kubernetes.sh
./kubernetes.sh
```
Configuration multinode
```sh
# Get the IP address and configure the Pod network
POD_NETWORK=$(ip addr show | grep 'inet' | awk '{print $2}' | grep -v -e '::' -e '127.0.0.1' -e '10.255.255.254' -e '172.17.0.1')
ENDPOINT=$(ip addr show | grep 'inet' | awk '{print $2}' | grep -v -e '::' -e '127.0.0.1' -e '10.255.255.254' -e '172.17.0.1' | cut -d'/' -f1)
echo "CONFIGURING POD NETWORK WITH IP: $POD_NETWORK"
echo "CONFIGURING POD NETWORK WITH IP: $ENDPOINT"
sudo kubeadm init --control-plane-endpoint $ENDPOINT:6443 --pod-network-cidr=$POD_NETWORK --cri-socket=unix:///var/run/cri-dockerd.sock --upload-certs --v=5  --ignore-preflight-errors=all
```

or

```sh
kubeadm init --config '~/kubeadm-config.yml' --upload-certs

```

```sh
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
```

Masters

```sh
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
controlPlaneEndpoint: "172.27.11.200:6443" 
networking:
  podSubnet: "192.168.0.0/16" 
  serviceSubnet: "10.96.0.0/12" 

---
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: "172.27.11.200" 
  bindPort: 6443 
nodeRegistration:
  criSocket: "unix:///var/run/cri-dockerd.sock"
  ignorePreflightErrors:
    - "all"
  name: "mastername" # 
```

### WINDOWS

```sh
winget install Kubernetes.kubectl
kubectl version --client
scp user@150.55.133.10:/etc/kubernetes/admin.conf C:\Users\<SeuUsuario>\kubeconfig-150.55.133.10
set KUBECONFIG=C:\Users\User\kubeconfig-150.55.133.10
set KUBECONFIG=C:\Users\<SeuUsuario>\kubeconfig-150.55.133.10;C:\Users\<SeuUsuario>\kubeconfig-150.55.133.20;C:\Users\<SeuUsuario>\kubeconfig-150.55.133.30
kubectl config view --merge --flatten > C:\Users\<SeuUsuario>\.kube\config
```


This Markdown file provides a step-by-step guide to setting up Docker, CRI-Docker, Kubernetes, and related components on a Linux system. It includes references to external sources for additional context.
#### Reference: [David Hwang](https://www.youtube.com/watch?v=o6bxo0Oeg6o)
