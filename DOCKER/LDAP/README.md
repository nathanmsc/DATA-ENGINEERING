### OPEN LDAP

OPEN LDAP CONTAINER
```sh
docker run -p 389:389 -p 636:636 --name openldap-server --hostname openldap-server --restart always --env LDAP_ORGANISATION="DOMAIN" --env LDAP_DOMAIN="domain.local" --env LDAP_ADMIN_PASSWORD="password" --detach osixia/openldap:latest

```

OPEN LDAP INTERFACE
```sh
docker run -p 6443:443 --name phpldapadmin --hostname phpldapadmin --link openldap-server:mindsetcloud --env PHPLDAPADMIN_LDAP_HOSTS=mindsetcloud --detach  osixia/phpldapadmin:latest
```
