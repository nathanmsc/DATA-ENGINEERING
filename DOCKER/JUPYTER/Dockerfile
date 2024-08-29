# Use an Python base image
FROM python:3.10-slim-buster

# Set environment variables
ENV USERNAME=jupyter
ENV HOME=/home/jupyter

# Install required packages and systemd
RUN apt-get update && \
    apt-get install -y sudo curl systemd

# Create user and configure sudo only if the user doesn't exist
RUN id -u $USERNAME &>/dev/null || adduser --disabled-password --gecos "" $USERNAME && \
    usermod -aG sudo $USERNAME && \
    mkdir /home/jupyter && \
    chown -R $USERNAME:$USERNAME /home/jupyter && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers

USER $USERNAME
WORKDIR $HOME
# Pull the desired model
RUN pip install jupyterlab
CMD ["jupyter", "lab"]
