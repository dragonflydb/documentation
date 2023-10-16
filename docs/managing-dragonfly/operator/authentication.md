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
authentication required
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

TLS-based authentication is a more secure way to secure your Dragonfly instance. In this method, you can set up a TLS certificate for your Dragonfly instance through a secret. The certificate is then used to authenticate the clients.