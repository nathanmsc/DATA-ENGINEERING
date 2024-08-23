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
echo "Running: ./kubernetes.sh"
curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/kubernetes.sh
sudo chmod +x kubernetes.sh
./kubernetes.sh
```

This Markdown file provides a step-by-step guide to setting up Docker, CRI-Docker, Kubernetes, and related components on a Linux system. It includes references to external sources for additional context.
Reference: [David Hwang](https://www.youtube.com/watch?v=o6bxo0Oeg6o)
