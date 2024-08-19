## _SSH CONFIGURE_

### install openssh-server and generate key
```sh
ssh-keyhen
```

### copy public key to another server
```sh
cat .ssh/id_rsa.pub
```

### create and paste content on another server id_rsa.pub
```sh
touch id_rsa.pub
cat id_rsa.pub >> authorized_keys
```

### set permissions
```sh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```
