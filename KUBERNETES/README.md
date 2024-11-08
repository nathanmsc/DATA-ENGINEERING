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

Masters
```sh
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: "v1.23.0" # Substitua pela versão desejada do Kubernetes
controlPlaneEndpoint: "172.27.11.200:6443" # IP e porta do frontend configurado no HAProxy
networking:
  podSubnet: "192.168.0.0/16" # Sub-rede para pods, ajuste conforme necessário
  serviceSubnet: "10.96.0.0/12" # Sub-rede para serviços, ajuste conforme necessário

---
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: "172.27.11.200" # Endereço de anúncio, ajuste conforme necessário
  bindPort: 6443 # Porta para bind
nodeRegistration:
  criSocket: "/var/run/dockershim.sock" # ou o caminho para o CRI correto (como containerd)
  name: "master-01" # Nome do nó, ajuste conforme necessário

```

This Markdown file provides a step-by-step guide to setting up Docker, CRI-Docker, Kubernetes, and related components on a Linux system. It includes references to external sources for additional context.
#### Reference: [David Hwang](https://www.youtube.com/watch?v=o6bxo0Oeg6o)
