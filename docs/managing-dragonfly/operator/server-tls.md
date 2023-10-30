---
sidebar_position: 5
---

# Dragonfly With Server TLS

This guide will walk you through setting up Dragonfly with TLS. With TLS enabled, you can have
encrypted communication between your clients and the Dragonfly instance.

## Prerequisites

- A Kubernetes cluster with kubectl configured to access it.
- [Dragonfly Operator](installation.md) installed in your cluster.

## Generate a Cert with Cert Manager

Cert Manager is a Kubernetes add-on to automate the management and issuance of TLS certificates from various issuing sources.
In this guide, we will use the self-signed issuer to generate a cert.

You can also skip this step and use the self-signed cert that is generated manually. The Operator expects
a relevant secret to be present with `tls.crt`, `tls.key` keys.

### Install Cert Manager

```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```


Create a self-signed issuer:

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

Request a certificate from the self-signed issuer:

```sh
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: dragonfly-sample
spec:
  # Secret names are always required.
  secretName: dragonfly-sample
  duration: 2160h # 90d
  renewBefore: 360h # 15d
  subject:
    organizations:
      - dragonfly-sample
  # The use of the common name field has been deprecated since 2000 and is
  # discouraged from being used.
  commonName: example.com
  privateKey:
    algorithm: RSA
    encoding: PKCS1
    size: 2048
  # At least one of a DNS Name, URI, or IP address is required.
  dnsNames:
    - dragonfly-sample.com
    - www.dragonfly-sample.com
  # Issuer references are always required.
  issuerRef:
    name: ca-issuer
    kind: Issuer
    group: cert-manager.io
EOF
```

## Dragonfly Instance With TLS

As atleast one auth mechanism is required, we will use the password auth mechanism:

```sh
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: dragonfly-password
type: Opaque
stringData:
  password: dragonfly
EOF
```

Create a Dragonfly instance with one at-least one auth mechanism as its needed when TLS is enabled.

```sh
kubectl apply -f - <<EOF
apiVersion: dragonflydb.io/v1alpha1
kind: Dragonfly
metadata:
  name: dragonfly-sample
spec:
    authentication:
      passwordFromSecret:
        name: dragonfly-password
        key: password
    replicas: 2
    tlsSecretRef:
      name: dragonfly-sample
EOF
```

Check the status of the Dragonfly instance:

```sh
kubectl describe dragonflies.dragonflydb.io dragonfly-sample
```

## Connecting to Dragonfly

The CA cert is stored in a secret named `dragonfly-sample` in the `default` namespace. We
use that to connect to Dragonfly. This is required as we are using a self-signed cert that
is not trusted by default.

Create a redis-cli container with the ca.crt

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
                    "-a",
                    "dragonfly",
                    "--tls",
                    "--cacert",
                    "/etc/ssl/ca.crt"
                ],
                "volumeMounts": [
                    {
                        "name": "ca-certs",
                        "mountPath": "/etc/ssl",
                        "readOnly": true
                    }
                ]
            }
        ],
        "volumes": [
            {
                "name": "ca-certs",
                "secret": {
                    "secretName": "dragonfly-sample",
                    "items": [
                        {
                            "key": "ca.crt",
                            "path": "ca.crt"
                        }
                    ]
                }
            }
        ]
    }
}'
```

You should see the redis-cli prompt, and you can run redis commands.
