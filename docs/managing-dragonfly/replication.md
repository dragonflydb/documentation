---
sidebar_position: 4
---

# Replication

## Managing Replicas

Dragonfly supports a primary/secondary replication model, similarly to Redis’s [replication](https://redis.io/topics/replication). When using replication, Dragonfly creates exact copies of the primary instance. Once configured properly, secondary instances reconnect to the primary any time their connections break and will always aim to remain an exact copy of the primary.

Dragonfly replication management API is compatible with Redis API and consists of two user-facing commands: ROLE and REPLICAOF (SLAVEOF).

If you’re not sure whether the Dragonfly instance you’re currently connected to is a primary instance or a replica, you can check by running the  `role ` command:

```bash
role
```

This command will return either  `master ` or  `replica `.

## Redis/Dragonfly replication
Dragonfly supports Redis -> Dragonfly replication to allow a convenient migration of Redis workloads to Dragonfly. We currently support data structures and replication protocol of Redis OSS up to version 6.2. The instructions below apply to this type of replication as well with only difference that the primary instance is a running Redis server.

## Dragonfly/Dragonfly replication
This replication process internally is vastly different from the original Redis replication algorithm, but from the outside, the API is kept the same to make it compatible with the current ecosystem.

To designate a Dragonfly instance as a replica of another instance on the fly, run the  `replicaof ` command. This command takes the intended primary server’s hostname or IP address and port as arguments:

```bash
replicaof hostname_or_IP port
```

If the server is already a replica of another primary, it will stop replicating the old server and immediately start synchronizing with the new one. It will also discard the old dataset.

To promote a replica back to being a primary, run the following `replicaof` command:
```bash
replicaof no one
```

This will stop the instance from replicating the primary server but will not discard the dataset it has already replicated. This syntax is useful in cases where the original primary fails. After running `replicaof no one` on a replica of the failed primary, the former replica can be used as the new primary and have its own replicas as a failsafe.

## Secure replication with TLS -- Prerequisites

Dragonfly supports replication over TLS. To make it work you need:

1. To configure your Dragonfly instance to use TLS. That includes getting or generating a server certificate.
2. To choose a method of authentication between the replica and the master. This can be either with a password or with client certificates.

Also note that we only support `.pem` files, any other format won't work with dragonfly.

You can use `OpenSSL` to generate the required certificates. For example, the process of generating a server certificate and signing it with a self-managed CA is as follows:

Generate Dragonfly's private key and certificate signing request (CSR):
```bash
openssl req -newkey rsa:4096 -nodes -keyout server-key.pem -out server-req.pem
```
This will prompt you to add additional details for the subject which contains information
related to the certificate. The attributes of the subject are key-value pairs and are the following:

- CN: CommonName
- OU: OrganizationalUnit
- O: Organization
- L: Locality
- S: StateOrProvinceName
- C: CountryName

The `-nodes` part means `no DES`, that is, do not encrypt the private key. For production use cases,
you should always consider encrypting private keys.

Finally, you should use the CA's private key to sign dragonfly's CSR and get back the signed certificate
```bash
openssl x509 -req -in server-req.pem -days 365 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem
```

The `ca-cert.pem` and `ca-key.pem` can be generated like in the first step described above. The same process applies for generating client keys.

When generating private keys, always be mindful about storing and provisioning them securely!

## Secure replication with TLS

To enable TLS for dragonfly, you must supply the following arguments:

```bash
dragonfly --tls --tls_key_file=server-key.pem --tls_cert_file=server-cert.pem --tls_ca_cert_file=ca-cert.pem
```

Start the replica on a different port (in this example the port is 6380, and the host is local host):
```bash
dragonfly --tls --tls_key_file=replica-client-key.pem --tls_cert_file=replica-client-cert.pem --tls_ca_cert_file=ca-cert.pem --tls_replication=true --port 6380
```

Finally, connect to the replica and issue a `REPLICAOF` command:

```bash
redis-cli --tls --key ./client-key.pem --cert ./client-cert.pem --cacert ./ca-cert.pem -p 6380

REPLICAOF LOCALHOST 6379
```
Now, replication works over TLS and is secure. This example assumes that `ca-cert.pem` is a root certificate
used to authenticate both the server and the client. For example, if the server is using a certificate
signed by a public CA this flag should not be passed as an argument to the replica.

## Non TLS connections over admin port on TLS configured dragonfly

Sometimes, it might be the case that both the master and the replica are on the same private network. For that case, you might want TLS for connections outside of the private network but have plaintext communication over the more secure private network. In cases like this you can disable tls replication specifically on the admin port:

Start master with:
```bash
dragonfly --tls --tls_key_file=server-key.pem --tls_cert_file=server-cert.pem --tls_ca_cert_file=ca-cert.pem -admin_port=6380 --no_tls_on_admin_port=true
```

Start replica with:
```bash
dragonfly --tls --tls_key_file=replica-client-key.pem --tls_cert_file=replica-client-cert.pem --tls_ca_cert_file=ca-cert.pem --port 6381 -admin_port=6382
```

And then issue a `REPLICAOF` command through the admin port via:

```bash
redis-cli -p 6382

REPLICAOF HOST 6380
```

from now on the replica *does not* communicate over TLS but incoming connections on ports `6379, 6381` require TLS and are considered secure.

## Monitoring Lag

Dragonfly defines the replication lag as the maximal amount of unacknowledged database among all shards. This metric is calculated by the master instance and is visible both as the `dragonfly_connected_replica_lag_records` field in the [prometheus metrics](./monitoring.md), and through the `INFO REPLICATION` command.
