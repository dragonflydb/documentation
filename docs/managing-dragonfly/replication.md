---
sidebar_position: 4
---

# Replication

## Managing Replication

Dragonfly supports a primary-replica high-availability model, similarly to Redis's [replication](https://redis.io/topics/replication).
When using replication, Dragonfly creates exact copies of the primary instance.
Once configured properly, replicas reconnect to the primary instance any time their connections break and will always aim to remain an exact copy of the primary.

The Dragonfly replication management API is compatible with the Redis API and consists of two main commands:
[`ROLE`](../command-reference/server-management/role.md) and [`REPLICAOF`](../command-reference/server-management/replicaof.md).
If you're not sure whether the Dragonfly instance you're currently connected to is a primary instance or a replica, you can check by running the `ROLE` command:

```bash
dragonfly$> ROLE
1) "master"
2) 1) 1) "172.19.0.4"
      2) "6379"
      3) "stable_sync"
```

This command will return either `master` or `replica` with additional information, depending on the role of the instance.

## Redis-Dragonfly Replication

Dragonfly supports Redis-Dragonfly replication to allow a convenient migration of Redis workloads to Dragonfly.
We currently support the data structures and replication protocol of Redis OSS up to version 6.2.
The instructions below apply to this type of replication as well, with the only difference being that the primary instance is a running Redis server.

## Dragonfly-Dragonfly Replication

This replication process internally is vastly different from the original Redis replication algorithm, but from the outside, the API is kept the same to make it compatible with the current ecosystem.

To designate a Dragonfly instance as a replica of another instance on the fly, run the `REPLICAOF` command.
This command takes the intended primary instance's hostname or IP address and port as arguments:

```bash
dragonfly$> REPLICAOF hostname_or_IP port
```

If the server is already a replica of another primary, it will stop replicating the old primary and immediately start synchronizing with the new one.
It will also discard the entire old dataset.

To promote a replica back to being a primary, run the following `REPLICAOF` command:

```bash
dragonfly$> REPLICAOF NO ONE
```

This will stop the instance from replicating the primary instance but will not discard the dataset it has already replicated.
This syntax is useful in cases where the original primary fails.
After running `REPLICAOF NO ONE` on a replica of the failed primary, the former replica can be used as the new primary and have its own replicas as a failsafe.

## Secure Replication with TLS

### Secure Replication Prerequisites

Dragonfly supports replication over TLS. To make it work, you need:

1. To configure your Dragonfly instance to use TLS. That includes getting or generating a server certificate.
2. To choose a method of authentication between the replica and the primary instance.
   This can be either with a password or with client certificates.

Also note that we only support `.pem` files.
Any other format won't work with Dragonfly.

You can use `OpenSSL` to generate the required certificates.
For example, the process of generating a server certificate and signing it with a self-managed CA is as follows:

Generate Dragonfly's private key and certificate signing request (CSR):

```bash
openssl req -newkey rsa:4096 -nodes -keyout server-key.pem -out server-req.pem
```

This will prompt you to add additional details for the subject which contains information related to the certificate.
The attributes of the subject are key-value pairs as follows:

- `CN`: CommonName
- `OU`: OrganizationalUnit
- `O`: Organization
- `L`: Locality
- `S`: StateOrProvinceName
- `C`: CountryName

The `-nodes` argument means `no DES`, that is, do not encrypt the private key.
**For production use cases, you should always consider encrypting private keys.**

Finally, you should use the CA's private key to sign Dragonfly's CSR and get back the signed certificate:

```bash
openssl x509 -req -in server-req.pem -days 365 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem
```

The `ca-cert.pem` and `ca-key.pem` can be generated like in the first step described above.
The same process applies for generating client keys.
**When generating private keys, always be mindful about storing and provisioning them securely!**

### Secure Replication Setup

To enable TLS for Dragonfly, you should supply the following arguments:

```bash
dragonfly --tls --tls_key_file=server-key.pem --tls_cert_file=server-cert.pem --tls_ca_cert_file=ca-cert.pem
```

Start the secondary Dragonfly instance on a different port (i.e., `6380`) with the following arguments:

```bash
dragonfly --tls --tls_key_file=replica-client-key.pem --tls_cert_file=replica-client-cert.pem --tls_ca_cert_file=ca-cert.pem --tls_replication=true --port 6380
```

Finally, connect to the secondary Dragonfly instance and issue the `REPLICAOF` command:

```bash
redis-cli --tls --key ./client-key.pem --cert ./client-cert.pem --cacert ./ca-cert.pem -p 6380

dragonfly$> REPLICAOF PRIMARY_HOST 6379
```

Now, the replication works over TLS and is secure.
This example assumes that `ca-cert.pem` is a root certificate used to authenticate both the server and the client.
For example, if the server is using a certificate signed by a public CA, this flag should not be passed as an argument to the replica.

## Non-TLS Connections over Admin Ports

In some scenarios, **both the primary instance and its replica may be located on the same private network.**
Under these circumstances, you might prefer to use TLS for connections that are external to the private network
while allowing plaintext communication within the secure confines of the private network.
For situations like these, it's possible to specifically disable TLS for replication on the admin port, as described below.

Start the primary instance with:

```bash
dragonfly --tls --tls_key_file=server-key.pem \
          --tls_cert_file=server-cert.pem \
          --tls_ca_cert_file=ca-cert.pem \
          --port 6379 -admin_port=6380 --no_tls_on_admin_port=true
```

Start the secondary Dragonfly instance with:

```bash
dragonfly --tls --tls_key_file=replica-client-key.pem \
          --tls_cert_file=replica-client-cert.pem \
          --tls_ca_cert_file=ca-cert.pem
          --port 6381 -admin_port=6382
```

Then, connect to the secondary Dragonfly instance and issue the `REPLICAOF` command via the admin port:

```bash
redis-cli -p 6382

dragonfly$> REPLICAOF PRIMARY_HOST 6380
```

From now on, the replica **does not** communicate with the primary instance over TLS.
But incoming connections on ports `6379` and `6381` still require TLS and are considered secure.

## Monitoring Replication Lag

Dragonfly defines the replication lag as the maximal amount of unacknowledged database among all shards.
This metric is calculated by the primary instance and is visible both as the `dragonfly_connected_replica_lag_records` field in the [Prometheus metrics](./monitoring.md)
as well as in the `INFO REPLICATION` command output as the `lag` field.

```bash
# On the primary instance:

dragonfly$> INFO REPLICATION
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6380,state=stable_sync,lag=0 # <- The replication lag is reported here.
master_replid:3ad69228e6973c1fc24805efb46d3f6eeeee4fde
```
