## download and install package
```sh
# wget https://repo.zabbix.com/zabbix/6.2/ubuntu-arm64/pool/main/z/zabbix-release/zabbix-release_6.2-2%2Bubuntu22.04_all.deb
# dpkg -i zabbix-release_6.2-2+ubuntu22.04_all.deb
# apt update
```

## install dependences on web server
```sh
# apt install zabbix-server-pgsql zabbix-frontend-php php8.1-pgsql zabbix-apache-conf zabbix-sql-scripts zabbix-agent
```

## create user and db on database server
```sh
# sudo -u postgres createuser --pwprompt uzabbix
# sudo -u postgres createdb -O zabbix zabbixdb
```

## run script on database server
```sh
# zcat /usr/share/zabbix-sql-scripts/postgresql/server.sql.gz | sudo -u uzabbix psql zabbixdb
```

## edit file on web server
```sh
vim /etc/zabbix/zabbix_server.conf
#DBPassword=password
```

## restart services on web server
```sh
# systemctl restart zabbix-server zabbix-agent apache2
# systemctl enable zabbix-server zabbix-agent apache2

```
