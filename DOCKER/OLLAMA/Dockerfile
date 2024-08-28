# Use an Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV USERNAME=ollama

# Install required packages and systemd
RUN apt-get update && \
    apt-get install -y sudo curl systemd && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    adduser --disabled-password --gecos "" $USERNAME && \
    usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers && \
    systemctl daemon-reload && \
    systemctl enable ollama && \
    ollama start &

# Pull the desired model
RUN ollama pull llama3.1:8b

# Set the default user
USER $USERNAME

# Expose the necessary port if Ollama uses one
EXPOSE 11434

# Start the Ollama service by default when the container runs
CMD ["ollama", "run", "llama3.1:8b"]
