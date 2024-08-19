docker run -d \
	--name postgres-server \
  --hostname postgres-server \
  -e POSTGRES_USER=user
	-e POSTGRES_PASSWORD="********" \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v /var/lib/postgresql/data:/var/lib/postgresql/data \
  --restart=always
  --net mindsetcloud-net
  --ip 192.168.32.2
	mindsetcloud/postgres:arm64
