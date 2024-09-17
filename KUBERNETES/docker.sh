# Clear the terminal screen
clear

# Install necessary certificates and utilities
echo "INSTALLING CERTIFICATES AND UTILITIES"
sudo apt-get update -y && sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    software-properties-common \
    apt-transport-https \
    lsb-release
sleep 2

# Clear the terminal screen
clear

# Install Docker's official GPG key
echo "INSTALLING DOCKER GPG KEY"
sudo mkdir -p /etc/apt/keyrings
if curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg; then
    echo "GPG key installed successfully."
else
    echo "Failed to install GPG key." >&2
    exit 1
fi
sleep 2

# Clear the terminal screen
clear

# Add Docker repository to APT sources
echo "ADDING DOCKER APT REPOSITORY"
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sleep 2

# Clear the terminal screen
clear

# Update package index and install Docker
echo "UPDATING PACKAGE INDEX AND INSTALLING DOCKER"
sudo apt-get update -y
if sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin; then
    echo "Docker installed successfully."
else
    echo "Failed to install Docker." >&2
    exit 1
fi
sleep 2

# Add the current user to the docker group
echo "ADDING USER TO DOCKER GROUP"
groups ${USER}
sudo usermod -aG docker ${USER}
if [ $? -eq 0 ]; then
    echo "User added to the docker group. Please log out and back in to apply the changes."
else
    echo "Failed to add user to docker group." >&2
    exit 1
fi
newgrp docker
sudo systemctl restart docker
sleep 2

# Final message
clear
echo $USER > /home/$USER/username
sudo -i
su $(cat /home/$(ls /home)/username)
docker ps
echo "DOCKER INSTALLATION COMPLETED SUCCESSFULLY"
