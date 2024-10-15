FROM ubuntu:latest

RUN apt-get update && \
    apt-get install sudo curl systemd build-essential -y
RUN curl -fsSL https://ollama.com/install.sh | sh

COPY password /tmp/password
RUN mkdir /home/ollama
RUN echo "ollama:$(cat /tmp/password)" | sudo chpasswd

RUN cp -r /etc/skel/. /home/ollama
RUN rm -rf /tmp/password
RUN usermod -aG sudo ollama
RUN chmod -R 0755 /home/ollama
RUN chown -R ollama:ollama /home/ollama

ENV HOME=/home/ollama
ENV USERNAME=ollama

RUN curl -O https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/main/DOCKER/OLLAMA/ollama.service
RUN mv ollama.service /etc/systemd/system/
RUN chown -R $USERNAME:$USERNAME /home/ollama
RUN chown -R $USERNAME:$USERNAME /etc/systemd/system/ollama.service
RUN chmod 0750 /etc/systemd/system/ollama.service

USER $USERNAME
ENV OLLAMA_HOST=0.0.0.0
RUN /etc/systemd/system/ollama.service enable
EXPOSE 11434
WORKDIR $HOME

CMD ["ollama", "serve"]
