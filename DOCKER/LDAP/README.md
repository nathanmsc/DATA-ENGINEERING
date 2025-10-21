### OPEN LDAP

### OPEN LDAP CONTAINER
```sh
sudo docker run -p 389:389 -p 636:636 --name openldap --env LDAP_ORGANISATION="Rescue Point" --env LDAP_DOMAIN="rescuepoint.com.br" --env LDAP_ADMIN_PASSWORD=<password> --detach osixia/openldap:latest

```

### OPEN LDAP INTERFACE
```sh
sudo docker run -p 6443:443 --name phpldapadmin --hostname phpldapadmin --link openldap:rescue --env PHPLDAPADMIN_LDAP_HOSTS=rescue --detach osixia/openldap:latest
```
