# Use an Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV USERNAME=ollama
ENV HOME=/home/ollama

# Install required packages and systemd
RUN apt-get update && \
    apt-get install -y sudo curl systemd

RUN curl -fsSL https://ollama.com/install.sh | sh

# Create user and configure sudo only if the user doesn't exist
RUN id -u $USERNAME &>/dev/null || adduser --disabled-password --gecos "" $USERNAME && \
    usermod -aG sudo $USERNAME && \
    mkdir /home/ollama && \
    chown -R $USERNAME:$USERNAME /home/ollama && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers

USER $USERNAME
WORKDIR $HOME
# Pull the desired model
CMD ["ollama", "start"]
