---
sidebar_position: 1
---

# Install Dragonfly Kubernetes Operator

Dragonfly Operator is a Kubernetes operator used to deploy and manage [Dragonfly](https://dragonflydb.io/) instances inside your Kubernetes clusters.
Main features include:

- Automatic failover
- Scaling Horizontally and Vertically
- Custom configuration options

Currently, Dragonfly Operator is in **Alpha**. You can find more information about Dragonfly
in the [official documentation](https://dragonflydb.io/docs/).

## Prerequisites

- Working Kubernetes cluster (tested with Kubernetes 1.19+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed and configured to connect to your cluster

## Installation

Make sure to have your Kubernetes cluster up and running. Dragonfly Operator can be installed by running

```sh
# Install CRDs
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/crd.yaml
# Install the operator
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```

By default, the operator will be installed in the `dragonfly-operator-system` namespace.

## Usage

### Creating a Dragonfly instance

To create a sample Dragonfly instance, you can run the following command:

```sh
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/config/samples/v1alpha1_dragonfly.yaml
```

This will create a Dragonfly instance with 3 replicas. You can check the status of the instance by running

```sh
kubectl describe dragonflies.dragonflydb.io dragonfly-sample
```

A service of the form `<dragonfly-name>.<namespace>.svc.cluster.local` will be created, that selects the master instance. You can use this service to connect to the cluster. As pods are added/removed, the service will automatically update to point to the new master.

#### Connecting with `redis-cli`

To connect to the cluster using `redis-cli`, you can run:

```sh
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-sample.default
```

This will create a temporary pod that runs `redis-cli` and connects to the cluster. After pressing `shift + R`, You can then run Redis commands as
usual. For example, to set a key and get it back, you can run

```sh
If you don't see a command prompt, try pressing enter.
dragonfly-sample.default:6379> GET 1
(nil)
dragonfly-sample.default:6379> SET 1 2
OK
dragonfly-sample.default:6379> GET 1
"2"
dragonfly-sample.default:6379> exit
pod "redis-cli" deleted
```

### Scaling up/down the number of replicas

To scale up/down the number of replicas, you can edit the `spec.replicas` field in the Dragonfly instance. For example, to scale up to 5 replicas, you can run

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"replicas":5}}'
```

### Passing Custom Dragonfly Arguments

To pass custom arguments to Dragonfly, you can edit the `spec.args` field in the Dragonfly instance. For example, to have
Dragonfly require a password, you can run

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"args":["--requirepass=supersecret"]}}'
```

### Vertically scaling the instance

To vertically scale the instance, you can edit the `spec.resources` field in the Dragonfly instance. For example, to increase the CPU limit to 2 cores, you can run

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"resources":{"requests":{"memory":"1Gi"},"limits":{"memory":"2Gi"}}}}'
```
