---
sidebar_position: 2
---

# Dragonfly Instance Authentication

This guide provides step-by-step instructions for setting up Dragonfly with authentication. Currently, Dragonfly supports two types of authentication:

- [Password-based authentication](#password-based-authentication) through a secret
- [TLS-based authentication](#tls-based-authentication) through a secret

## Prerequisites

- A Kubernetes cluster with [Dragonfly installed](./installation.md)

## Password-based authentication

Password-based authentication is the simplest way to secure your Dragonfly instance. In this method, you can set a password for your Dragonfly instance through a secret. The password is then used to authenticate the clients.

### Create a secret

```bash
kubectl create secret generic dragonfly-auth --from-literal=password=dragonfly
```

### Deploy Dragonfly with authentication

```bash
kubectl apply -f - <<EOF
apiVersion: dragonflydb.io/v1alpha1
kind: Dragonfly
metadata:
  name: dragonfly-auth
spec:
    authentication:
      passwordFromSecret:
        name: dragonfly-auth
        key: password
    replicas: 2
EOF
```

### Check the status of the Dragonfly instance

```bash
kubectl describe dragonflies.dragonflydb.io dragonfly-auth
```

### Connecting to Dragonfly

```bash
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-auth.default
if you don't see a command prompt, try pressing enter.
dragonfly-auth.default:6379> GET 1
(error) NOAUTH Authentication required. 
dragonfly-auth.default:6379> AUTH dragonfly
OK
dragonfly-auth.default:6379> GET 1
(nil)
dragonfly-auth.default:6379> SET 1 2
OK
dragonfly-auth.default:6379> GET 1
"2"
dragonfly-auth.default:6379> exit
```

## TLS-based authentication

TLS-based authentication is a more secure way to secure your Dragonfly instance. First, you need TLS configured on your Dragonfly instance. Then,
you can specify a list of CA certificates that are trusted by the Dragonfly instance. The clients must present a certificate signed by one of the
trusted CAs to connect to the Dragonfly instance.

### Create a TLS secret for Dragonfly through cert-manager

#### Install cert-manager

```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

#### Create a self-signed certificate

```sh
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: ca-issuer
spec:
  selfSigned: {}
EOF
```

#### Request a TLS certificate

```sh
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: dragonfly-sample
spec:
  secretName: dragonfly-sample
  duration: 2160h # 90d
  renewBefore: 360h # 15d
  subject:
    organizations:
      - dragonfly-sample
  privateKey:
    algorithm: RSA
    encoding: PKCS1
    size: 2048
  dnsNames:
    - dragonfly-sample.com
    - www.dragonfly-sample.com
  issuerRef:
    name: ca-issuer
    kind: Issuer
    group: cert-manager.io
EOF
```

### Generate a client certificate signed by a client CA

#### Create a Client CA

```sh
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: client-ca-issuer
spec:
  selfSigned: {}
EOF
```

#### Request a Client certificate

```sh
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: dragonfly-client-ca
spec:
    secretName: dragonfly-client-ca
    duration: 2160h # 90d
    renewBefore: 360h # 15d
    subject:
        organizations:
        - dragonfly-client-ca
    privateKey:
        algorithm: RSA
        encoding: PKCS1
        size: 2048
    dnsNames:
        - dragonfly-client-ca.com
        - www.dragonfly-client-ca.com
    usages:
        - client auth
    issuerRef:
        name: client-ca-issuer
        kind: Issuer
        group: cert-manager.io
EOF
```

### Create a Dragonfly instance with TLS

```sh
kubectl apply -f - <<EOF
apiVersion: dragonflydb.io/v1alpha1
kind: Dragonfly
metadata:
  name: dragonfly-sample
spec:
    authentication:
      clientCaCertSecret:
        name: dragonfly-client-ca
        key: ca.crt
    replicas: 2
    tlsSecretRef:
      name: dragonfly-sample
EOF
```

### Verify the Dragonfly instance is ready

```sh
kubectl describe dragonflies.dragonflydb.io dragonfly-sample
```

### Connecting to Dragonfly With TLS

You should be able to connect to the Dragonfly instance only if you have a client certificate signed by the client CA.

```sh
kubectl run -it --rm redis-cli --image=redis:7.0.10 --restart=Never --overrides='
{
    "spec": {
        "containers": [
            {
                "name": "redis-cli",
                "image": "redis:7.0.10",
                "tty": true,
                "stdin": true,
                "command": [
                    "redis-cli",
                    "-h",
                    "dragonfly-sample.default",
                    "--tls",
                    "--cacert",
                    "/etc/ssl/ca.crt",
                    "--cert",
                    "/etc/tls/tls.crt",
                    "--key",
                    "/etc/tls/tls.key"
                ],
                "volumeMounts": [
                    {
                        "name": "ca-certs",
                        "mountPath": "/etc/ssl",
                        "readOnly": true
                    },
                    {
                        "name": "client-certs",
                        "mountPath": "/etc/tls",
                        "readOnly": true
                    }
                ]
            }
        ],
        "volumes": [
            {
                "name": "ca-certs",
                "secret": {
                    "secretName": "dragonfly-sample"
                }
            },
            {
                "name": "client-certs",
                "secret": {
                    "secretName": "dragonfly-client-ca"
                }
            }
        ]
    }
}'
```
