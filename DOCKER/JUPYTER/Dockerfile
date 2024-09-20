FROM python:3.10-slim-buster
RUN apt update && apt upgrade -y
RUN apt install -y python3-venv sudo whois vim
RUN mkdir /home/jupyter
ARG password=.jupyter.
RUN secret=$(perl -e 'print crypt($ARGV[0], "password")' $password) && useradd jupyter -p $secret
RUN cp -r /etc/skel/. /home/jupyter
RUN usermod -aG sudo jupyter
RUN chmod -R 0755 /home/jupyter
RUN chown -R jupyter:jupyter /home/jupyter
USER jupyter
WORKDIR /home/jupyter
RUN /bin/bash -c 'python3 -m venv /home/jupyter/.jupyter.'
RUN /bin/bash -c 'source /home/jupyter/.jupyter./bin/activate && pip3 install jupyterlab'
RUN echo "source /home/jupyter/.jupyter./bin/activate" >> /home/jupyter/.bashrc
EXPOSE 8888
CMD ["/bin/bash", "-c", "source /home/jupyter/.jupyter./bin/activate && jupyter lab --port=8888 --no-browser --ip=0.0.0.0 --allow-root"]
