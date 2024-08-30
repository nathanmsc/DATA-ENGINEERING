FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y sudo curl systemd
RUN curl -fsSL https://ollama.com/install.sh | sh

ENV HOME=/home/ollama
ENV USERNAME=ollama

RUN curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/DOCKER/OLLAMA/ollama.service
RUN mv ollama.service /etc/systemd/system/
RUN  echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers
RUN mkdir /home/ollama
RUN chown -R $USERNAME:$USERNAME /home/ollama
USER $USERNAME
ENV OLLAMA_HOST=0.0.0.0

RUN sudo chown -R $USERNAME:$USERNAME /etc/systemd/system/ollama.service
RUN sudo chmod 0750 /etc/systemd/system/ollama.service
RUN /etc/systemd/system/ollama.service enable
EXPOSE 11434
WORKDIR $HOME

CMD ["ollama", "serve"]
