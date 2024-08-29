# Use an Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV USERNAME=ollama
ENV HOME=/home/ollama
ENV OLLAMA_HOST=0.0.0.0

# Install required packages and systemd
RUN apt-get update && \
    apt-get install -y sudo curl systemd

RUN curl -fsSL https://ollama.com/install.sh | sh

# Create user and configure sudo only if the user doesn't exist
RUN id -u $UiSERNAME &>/dev/null || adduser --disabled-password --gecos "" $USERNAME && \
    usermod -aG sudo $USERNAME && \
    mkdir /home/ollama && \
    chown -R $USERNAME:$USERNAME /home/ollama && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers

USER $USERNAME
WORKDIR $HOME

EXPOSE 11434

CMD ["ollama", "start"]
