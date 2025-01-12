
# Kubernetes and Docker Setup Guide

This guide provides a step-by-step walkthrough for setting up Docker, CRI-Docker, Kubernetes, and related tools on a Linux system. It includes configurations for a single-node or multi-node Kubernetes cluster. 

---

## Prerequisites

Before proceeding, ensure the following:

1. **Disable Swap**:
   ```bash
   sudo swapoff -a
   sudo sed -i '/swap/d' /etc/fstab
   ```

2. **Install Docker**:
   Refer to the Docker installation instructions for your distribution.

3. **Install Go**:
   Install the latest version of Go as required by Kubernetes.

---

## Kubernetes Setup Script

### Installation

This script automates the installation of Kubernetes, Docker, and Golang.

#### Direct Execution:
```bash
echo "INSTALLING KUBERNETES, DOCKER AND GOLANG"
curl -fsSL https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/kubernetes.sh | sh
```

#### Manual Execution:
```bash
echo "Running: ./kubernetes.sh"
curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/kubernetes.sh
sudo chmod +x kubernetes.sh
./kubernetes.sh
```

---

## Multi-Node Configuration

### Master Node Setup

Configure the master node with the following:

```bash
#CONFIGURATION ON ONE MASTER
export $ENDPOINT=<ip-node-master>
export $POD_NETWORK=<ip-network\mask>
sudo kubeadm init \
  --control-plane-endpoint $ENDPOINT:6443 \
  --pod-network-cidr=$POD_NETWORK \
  --apiserver-advertise-address=<ip-this-server> \
  --cri-socket=unix:///var/run/cri-dockerd.sock \
  --upload-certs \
  --v=5 \
  --ignore-preflight-errors=all
```

Configure anothers nodes with the following:

```bash
#CONFIGURATION ON ANOTHER CONTROLPLANE
export $ENDPOINT=<ip-node-master>
sudo kubeadm join $ENDPOINT:6443 --apiserver-advertise-address 172.16.2.104 --token <TOKEN> \
        --discovery-token-ca-cert-hash <HASH> \
        --control-plane --certificate-key <CERTIFICATE> --cri-socket=unix:///var/run/cri-dockerd.sock --v=5  --ignore-preflight-errors=all
```

### Worker Node Setup

After initializing the master node, join worker nodes using the generated `kubeadm join` command:

```bash
kubeadm join <CONTROL_PLANE_IP>:6443 \
  --apiserver-advertise-address=<ip-this-server> \
  --token <TOKEN> \
  --discovery-token-ca-cert-hash sha256:<HASH> \
  --cri-socket=unix:///var/run/cri-dockerd.sock \
  --v=5 \
  --ignore-preflight-errors=all
```


---

## Configuration Using YAML

### Initialize with Config File

```bash
kubeadm init --config '~/kubeadm-config.yml' --upload-certs
```

### Sample `kubeadm-config.yml`

```yaml
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
  name: "mastername"
```

---

## Post-Setup Configuration

### Configure `kubectl`

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
sleep 4
```

### Install and Configure Calico for Networking

```bash
echo "INSTALLING AND CONFIGURING CALICO"
curl https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/calico.yaml -O
kubectl apply -f calico.yaml
sleep 2
```

### Update Kube Proxy Configuration

Edit the `kube-proxy` ConfigMap to enable `ipvs` mode:

```bash
kubectl edit configmap -n kube-system kube-proxy
```

Modify the configuration:

```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  strictARP: true
```

---

## Metallb Installation

### Deploy Metallb

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml -n metallb-system
```

### Metallb Configuration

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: ip-address-pool
  namespace: metallb-system
spec:
  addresses:
  - 172.16.2.170-172.16.2.189
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: l2-advertisement
  namespace: metallb-system
spec:
  ipAddressPools:
  - ip-address-pool
```

---

## Nginx Ingress Controller

Deploy the Nginx Ingress Controller:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0/deploy/static/provider/baremetal/deploy.yaml
```

---

## Configuring `kubectl` on Windows

### Install `kubectl`

```bash
winget install Kubernetes.kubectl
kubectl version --client
```

### Transfer Configuration File

```bash
scp user@150.55.133.10:/etc/kubernetes/admin.conf C:\Users\<YourUsername>\kubeconfig-150.55.133.10
```

### Set KUBECONFIG Environment Variable

```bash
set KUBECONFIG=C:\Users\<YourUsername>\kubeconfig-150.55.133.10
set KUBECONFIG=C:\Users\<YourUsername>\kubeconfig-150.55.133.10;C:\Users\<YourUsername>\kubeconfig-150.55.133.20;C:\Users\<YourUsername>\kubeconfig-150.55.133.30
kubectl config view --merge --flatten > C:\Users\<YourUsername>\.kube\config
```

---

## References

- [David Hwang](https://www.youtube.com/watch?v=o6bxo0Oeg6o)
- [Multi-Master Setup](https://www.youtube.com/watch?v=SueeqeioyKY&t=805s)
- [Kubeadm HA](https://github.com/justmeandopensource/kubernetes/tree/master/kubeadm-ha-keepalived-haproxy/external-keepalived-haproxy)
- [Ingress Nginx and Metallb](https://www.youtube.com/watch?v=cO8TEEashIk)
- [Metallb Documentation](https://metallb.io/installation)
