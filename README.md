<div>
  <img src="https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/DOCKER/ZABBIX/src/img/logo.svg" alt="Logo" width="18%" style="margin-right: 1%;"/>
  <img src="https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/DOCKER/ZABBIX/src/img/marca.svg" alt="Brand" width="80%" style="margin-left: 1%;"/>
</div>

<div align="center">
<p align="right">
  <h1>Transforming Data into Powerful Insights 🌐</h1>
</p>
</div>

### DATA ENGINEERING TOOLS AND INFRASTRUCTURE

By leveraging Kubernetes and containerization, organizations can build a resilient, scalable, and secure infrastructure for data engineering. This setup not only enhances the efficiency of data processing and analysis but also ensures adaptability to evolving challenges, providing a robust foundation for data-driven decision-making.

---

## Table of Contents

* [Kubernetes](https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/KUBERNETES/README.md)
* [Docker Containers](https://github.com/nathanmsc/DATA-ENGINEERING/tree/main/DOCKER)
* [Contributing](#contributing)
* [License](#license)

---

# 🔧 Kubernetes and Docker Setup Guide

This guide provides a comprehensive step-by-step process to set up Docker, CRI-Docker, Kubernetes, and related tools on a Linux system. It includes configurations for single-node or multi-node Kubernetes clusters.

---

## ⚡️ Prerequisites

Before you begin, ensure the following steps:

### ❌ Disable Swap

```bash
sudo swapoff -a
sudo sed -i '/swap/d' /etc/fstab
```

### 📦 Install Docker

Refer to the Docker installation guide for your distribution.

### 🌟 Install Go

Install the latest version of Go as required for Kubernetes.

---

## ⚙️ Kubernetes Installation Script

### 🔄 Automatic Installation

```bash
echo "INSTALLING KUBERNETES, DOCKER AND GOLANG"
curl -fsSL https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/SCRIPTS/kubernetes.sh | sh
```

### 🔧 Manual Execution

```bash
echo "Running: ./kubernetes.sh"
curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/SCRIPTS/kubernetes.sh
sudo chmod +x kubernetes.sh
./kubernetes.sh
```

---

## 👥 Multi-Node Configuration

### 🔍 Master Node Configuration

```bash
export ENDPOINT=<ip-node-master>
export POD_NETWORK=<ip-network\mask>
sudo kubeadm init \
  --control-plane-endpoint $ENDPOINT:6443 \
  --pod-network-cidr=$POD_NETWORK \
  --apiserver-advertise-address=<ip-this-server> \
  --cri-socket=unix:///var/run/cri-dockerd.sock \
  --upload-certs \
  --v=5 \
  --ignore-preflight-errors=all
```

### 🔗 Other Master Nodes Configuration

```bash
export ENDPOINT=<ip-node-master>
kubeadm join <CONTROL_PLANE_IP>:6443 \
  --apiserver-advertise-address=<ip-this-server> \
  --token <TOKEN> \
  --discovery-token-ca-cert-hash sha256:<HASH> \
  --cri-socket=unix:///var/run/cri-dockerd.sock \
  --v=5 \
  --ignore-preflight-errors=all
```

### 🌍 Worker Node Configuration

```bash
kubeadm join <CONTROL_PLANE_IP>:6443 --token <TOKEN> \
        --discovery-token-ca-cert-hash <HASH> --cri-socket=unix:///var/run/cri-dockerd.sock \
        --v=5  --ignore-preflight-errors=all
```

---

## 📂 YAML Configuration

### 🗓️ Initialize with Config File

```bash
kubeadm init --config '~/kubeadm-config.yml' --upload-certs
```

### 🔢 Example `kubeadm-config.yml`

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

## 🗖️ Post-Setup Configuration

### 🔧 Configure `kubectl`

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
sleep 4
```

### 👥 Set Role for Worker Nodes

```bash
kubectl label nodes worker-01 node-role.kubernetes.io/worker=worker-plane
```

### 🚀 Install and Configure Calico

```bash
echo "INSTALLING AND CONFIGURING CALICO"
curl https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/calico.yaml -O
kubectl apply -f calico.yaml
sleep 2
```

### 🖊️ Update Kube Proxy Configuration

```bash
kubectl edit configmap -n kube-system kube-proxy
```

Adjust to:

```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  strictARP: true
```

---

## 🚀 Install Metallb

### 🔧 Deploy Metallb

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml -n metallb-system
```

### 🔢 Metallb Configuration

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

## 🌐 Nginx Ingress Controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0/deploy/static/provider/baremetal/deploy.yaml
```

---

## 📂 Local Path Provisioner

### 🔧 Deploy Local Path Provisioner

```bash
kubectl -f https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/refs/heads/main/KUBERNETES/SCRIPTS/local-path.yaml apply
```

### 🔍 Set Storage Class as Default

```bash
kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

Or edit via YAML:

```bash
kubectl edit sc local-path
```

Adjust annotation:

```yaml
annotations:
  storageclass.kubernetes.io/is-default-class: "true"
```

### 🏠 Set Destination Path

```bash
kubectl -n local-path-storage edit configmap local-path-config
```

Adjust to:

```yaml
nodePathMap:
  - node: "DEFAULT_PATH_FOR_NON_LISTED_NODES"
    paths:
      - "/mnt/storage/local-path-provisioner"
```

---

## 💻 Configure `kubectl` on Windows

### ⚙️ Install `kubectl`

```bash
winget install Kubernetes.kubectl
kubectl version --client
```

### 📦 Transfer Configuration File

```bash
scp user@150.55.133.10:/etc/kubernetes/admin.conf C:\Users\<YourUsername>\kubeconfig-150.55.133.10
```

### 🔧 Set KUBECONFIG Environment Variable

```bash
set KUBECONFIG=C:\Users\<YourUsername>\kubeconfig-150.55.133.10
set KUBECONFIG=C:\Users\<YourUsername>\kubeconfig-150.55.133.10;C:\Users\<YourUsername>\kubeconfig-150.55.133.20;C:\Users\<YourUsername>\kubeconfig-150.55.133.30
kubectl config view --merge --flatten > C:\Users\<YourUsername>\.kube\config
```

---

## 🔗 References

* [David Hwang](https://www.youtube.com/watch?v=o6bxo0Oeg6o)
* [Multi-Master Setup](https://www.youtube.com/watch?v=SueeqeioyKY&t=805s)
* [Kubeadm HA](https://github.com/justmeandopensource/kubernetes/tree/master/kubeadm-ha-keepalived-haproxy/external-keepalived-haproxy)
* [Ingress Nginx and Metallb](https://www.youtube.com/watch?v=cO8TEEashIk)
* [Install and Configure Metallb](https://www.youtube.com/watch?v=7P9oMMg_djQ)
* [Metallb Documentation](https://metallb.io/installation)

---

## 🤝 Contributing

Contributions are welcome! Follow the guidelines in [CONTRIBUTING.md](https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/KUBERNETES/SCRIPTS/CONTRIBUTING.md).

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

🌟 Optimized guide with icons for better visualization and navigation.
