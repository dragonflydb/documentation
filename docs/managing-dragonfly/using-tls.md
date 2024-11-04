---
sidebar_position: 9
---

# Using Dragonfly with TLS

If you deploy Dragonfly over an endpoint that's connected to the internet,
you probably need to protect your data from leaking or being intercepted.
In order to support that, Dragonfly can serve your data over TLS,
an ISO-standardized protocol that provides encryption and authentication.

In this documentation, we'll show how easy it is to configure Dragonfly to use TLS.
To get a valid TLS certificate, we're going to assume that you have a shell open on an Ubuntu server and a DNS address that points to this server.
This DNS address will then be used to server our data store.

## Getting a Certificate

We'll provision a TLS certificate using a Python program called [`certbot`](https://github.com/certbot/certbot) that was made by [Let's Encrypt](https://letsencrypt.org/).
Let's use it!

1. Install Python and Nginx:

    ```bash
    $> sudo apt install -y nginx-light python3 python3-venv libaugeas0
    ```

2. Create a virtual environment and install certbot:

    ```bash
    $> python3 -m venv certbot
    $> certbot/bin/pip install certbot certbot-nginx
    ```

3. Now run `certbot` as root:

    ```bash
    $> sudo ./certbot/bin/certbot
    ```

You'll have to enter the URL that we want to use that points to the server,
in our case, `dfly.scalable-meteorite-collections.com`.
If all went well, the private key and the certificate are now located in `/etc/letsencrypt/live/`.

## Running Dragonfly

Choose a password for authenticating users to the data store:

```bash
$> export DFLY_PASS_TOKEN=<your_password>
```

We can now start Dragonfly on our server with TLS enabled:

```bash
$> sudo ./dragonfly --tls \
        --tls_key_file=/etc/letsencrypt/live/dfly.scalable-meteorite-collections.com/privkey.pem \
        --tls_cert_file=/etc/letsencrypt/live/dfly.scalable-meteorite-collections.com/fullchain.pem \
        --requirepass=${DFLY_PASS_TOKEN}
```

And connect to see that the data store is working properly:

```bash
$> redis-cli --tls -h dfly.scalable-meteorite-collections.com -a ${DFLY_PASS_TOKEN}
```

```bash
dragonfly$> SET anchdrite 33.7
OK
dragonfly$> SET pallasite 19.1
OK
dragonfly$> GET anchdrite
"33.7"
```

## Client Authentication with TLS

Instead of using passwords, **client certificates** can also be used to authenticate clients.
Since you'll be managing the certificates in this case, you won't need to use Let's Encrypt.
Assuming you have the required certificates, you can configure Dragonfly to require client certificates like this:

```bash
$> sudo ./dragonfly --tls \
        --tls_key_file=/etc/mycerts/server_key.pem \
        --tls_cert_file=/etc/mycerts/server_cert.pem \
        --tls_ca_cert_file=/etc/mycerts/clients_root_ca.pem
```

And connect with a client certificate like this:

```bash
$> redis-cli --tls -h dfly.scalable-meteorite-collections.com \
         --key /etc/mycerts/client_priv.pem \
         --cert /etc/mycerts/client_cert.pem
```

## Certificate Rotation without Downtime

To rotate the certificate of an existing Dragonfly server configured with TLS, you need to:

1. Update the `tls_key_file`, `tls_cert_file`, `tls_ca_cert_file` server flags according to your new TLS configuration.
2. Use the `CONFIG SET tls true` command to reload Dragonfly TLS configuration without downtime:

  ```bash
  $> redis-cli --tls -h dfly.scalable-meteorite-collections.com -a ${DFLY_PASS_TOKEN} \
    CONFIG SET tls true
  ```
