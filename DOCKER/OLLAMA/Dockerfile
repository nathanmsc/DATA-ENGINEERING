FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y sudo curl systemd
RUN curl -fsSL https://ollama.com/install.sh | sh

ENV USERNAME=ollama
RUN curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/DOCKER/OLLAMA/ollama.service
RUN mv ollama.service /etc/systemd/system/
RUN  echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers

USER $USERNAME
ENV OLLAMA_HOST=172.17.0.2

RUN sudo chown -R $USERNAME:$USERNAME /etc/systemd/system/ollama.service
RUN sudo chmod 0750 /etc/systemd/system/ollama.service
RUN /etc/systemd/system/ollama.service enable
EXPOSE 11434
WORKDIR ~
CMD ["ollama", "serve"]
