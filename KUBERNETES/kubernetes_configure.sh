# Get the IP address and configure the Pod network
IP_ADDRESS=$(ip addr show | grep 'inet' | awk '{print $2}' | grep -v -e '::' -e '127.0.0.1' -e '10.255.255.254' -e '172.17.0.1')
ENDPOINT=$(ip addr show | grep 'inet' | awk '{print $2}' | grep -v -e '::' -e '127.0.0.1' -e '10.255.255.254' -e '172.17.0.1' | cut -d'/' -f1)
echo "CONFIGURING POD NETWORK WITH IP: $IP_ADDRESS"
sudo kubeadm init --control-plane-endpoint $ENDPOINT:6443 --pod-network-cidr=$IP_ADDRESS --apiserver-advertise-address <ip-host> --cri-socket=unix:///var/run/cri-dockerd.sock --v=5  --ignore-preflight-errors=all

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
