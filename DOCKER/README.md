
# Docker Installation Guide

This guide provides step-by-step instructions for installing Docker on Ubuntu and setting up Docker Compose.

---

## Installing Docker on Ubuntu

### Option 1: Install via Script

Use the following command to quickly install Docker using a script:

```sh
curl -fsSL https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/KUBERNETES/docker.sh | sh
```

---

### Option 2: Manual Installation

#### Step 1: Update System and Install Dependencies

Run these commands to update the system and install the necessary packages:

```sh
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    software-properties-common \
    apt-transport-https \
    lsb-release
```

#### Step 2: Add Docker's Official GPG Key

Create a directory for storing the GPG key and add Docker's official GPG key:

```sh
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

#### Step 3: Add Docker's Repository

Add the Docker repository to your system:

```sh
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update the package index:

```sh
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
```

#### Step 4: Install Docker

Run the following commands to install Docker and verify the installation:

```sh
apt-cache policy docker-ce
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#### Step 5: Add User to the Docker Group

To avoid using `sudo` with Docker commands, add your user to the Docker group:

```sh
sudo usermod -aG docker ${USER}
```

---

## Installing Docker Compose

Docker Compose allows you to define and manage multi-container Docker applications.

### Step 1: Download Docker Compose

Download the Docker Compose binary and make it executable:

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Verify the Installation

Check the version to confirm Docker Compose is installed:

```sh
docker-compose --version
```

---

## Additional Docker Commands

### Get Container ID

Retrieve the ID of a specific container:

```sh
docker inspect --format="{{.Id}}" container
```

### Edit Container Configuration

To modify the container's configuration, edit the container file by its ID:

```sh
vim /var/lib/docker/containers/<ID>
```
