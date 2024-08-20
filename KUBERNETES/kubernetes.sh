clear
echo "UPDATE PACKAGES"
echo https://www.youtube.com/watch?v=o6bxo0Oeg6o
sudo apt update -y
sleep 2

clear
echo "INSTALL DOCKER FROM docker.sh FILE"
echo "./docker.sh"
#./docker.sh
sleep 2

clear
echo "INSTALL GIT"
sudo apt install git-all -y
sleep 2

clear
echo "INSTALL GO LANGUAGE"
sudo apt install golang-go -y
sleep 2

clear
echo "INSTALL CRI-DOCKER"
echo https://github.com/Mirantis/cri-dockerd
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

clear
echo "RELOAD DEAMON"
sudo systemd daemon-reload
sudo systemd enable cri-docker.service
sudo systemd enable --now cri-docker.socket
sleep 2

clear
echo "GET MIRROR K8S"
echo https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sleep 2

clear
echo "INSTALL KUBEADM AND KUBECTL"
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemd enable --now kubelet
sleep 2

clear
IP_ADDRESS=$(ip addr show | grep 'inet' | awk '{print $2}' | grep -v -e '::' -e '127.0.0.1')
echo "CONFIGURE POD NETWORK $(IP_ADDRESS)"
sudo kubeadm init --pod-network-cidr=$IP_ADDRESS --cri-socket=unix:///var/run/cri-dockerd.sock
#sudo kubeadm init --pod-network-cidr=$IP_ADDRESS --cri-socket=unix:///var/run/cri-dockerd.sock --ignore-preflight-errors=all
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
sleep 4

clear
echo "INSTALL AND CONFIGURE CALICO"
echo https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises
curl https://raw.githubusercontent.com/projectcalico/calico/v3.28.1/manifests/calico.yaml -O
kubectl apply -f calico.yaml
sleep 2

clear
echo "VALIDATE K8S INSTALL"
kubectl get pods -A
echo "sudo kubeadm init --control-plane-endpoint 132.145.141.255:6443 --pod-network-cidr=$(IP_ADDRESS) --cri-socket=unix:///var/run/cri-dockerd.sock --v=5"
echo "kubeadm join 150.136.44.198:6443 --token 6ide5b.bixu3kopmyuchphx \
        --discovery-token-ca-cert-hash sha256:1ff30e3737f162cf959bf9de942ce6e91715b346f63160a6602b6318661edad0 --cri-socket=unix:///var/run/cri-dockerd.sock"
