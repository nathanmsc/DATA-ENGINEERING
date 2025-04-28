## N8N

### DOCKER CLI

```sh
docker volume create n8n_data

docker run -it --rm \
 --name n8n \
 --hostname n8n-server \
 --net network \
 --ip 172.20.1.101  \
 -p 5678:5678 \
 -v n8n_data:/home/node/.n8n \
 docker.n8n.io/n8nio/n8n \
 start --tunnel
```

### DOCKER COMPESE FILE
```yaml
version: '3.8'

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    hostname: n8n-server
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DATABASE}
      - DB_POSTGRESDB_HOST=${POSTGRES_HOST}
      - DB_POSTGRESDB_PORT=${POSTGRES_PORT}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_SCHEMA=${POSTGRES_SCHEMA}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      network:
        ipv4_address: 172.20.1.101
    restart: unless-stopped

volumes:
  n8n_data:

networks:
  network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

```
