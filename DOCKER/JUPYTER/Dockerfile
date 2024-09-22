FROM python:3.12-slim-bookworm
RUN apt update && apt upgrade -y
RUN apt install curl sudo default-jdk build-essential -y
COPY password /tmp/password
RUN mkdir /home/jupyter
RUN secret=$(perl -e 'print crypt($ARGV[0], "password")' $(cat /tmp/password)) && useradd jupyter -p $secret
RUN cp -r /etc/skel/. /home/jupyter
RUN rm -rf /tmp/password
RUN usermod -aG sudo jupyter
RUN chmod -R 0755 /home/jupyter
RUN chown -R jupyter:jupyter /home/jupyter
USER jupyter
WORKDIR /home/jupyter
RUN /bin/bash -c 'curl -fsSL https://astral.sh/uv/install.sh | sh'
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="/home/jupyter/.cargo/bin:$PATH"
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN /bin/bash -c 'uv venv /home/jupyter/.jupyter.'
RUN /bin/bash -c 'source /home/jupyter/.jupyter./bin/activate && uv pip install jupyterlab pyspark'
RUN echo "source /home/jupyter/.jupyter./bin/activate" >> /home/jupyter/.bashrc
EXPOSE 8888
CMD ["/bin/bash", "-c", "source /home/jupyter/.jupyter./bin/activate && jupyter lab --port=8888 --no-browser --ip=0.0.0.0 --allow-root"]
