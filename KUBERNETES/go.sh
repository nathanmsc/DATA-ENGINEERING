clear
echo "INSTALLING GO LANGUAGE"

if sudo snap install go --classic; then
    echo "SUCCESSFUL INSTALLATION VIA SNAP"
    
elif git clone https://go.googlesource.com/go goroot && \
    cd goroot/src && \
    ./all.bash; then
    echo "SUCCESSFUL INSTALLATION VIA SOURCE"

elif sudo apt install golang-go -y; then
    echo "SUCCESSFUL INSTALLATION VIA APT"

elif wget https://go.dev/dl/go1.22.6.linux-amd64.tar.gz && \
    sudo tar -C /usr/local -xzf go1.22.6.linux-amd64.tar.gz && \
    export GOROOT_BOOTSTRAP=/usr/local/go && \
    git clone https://go.googlesource.com/go goroot && \
    cd ~/goroot/src && ./all.bash && rm -rf ~/goroot; then
    echo "SUCCESSFUL INSTALLATION VIA MANUAL DOWNLOAD"

else
    echo "GO LANGUAGE NOT INSTALLED"
    sleep 2
fi

