---
sidebar_position: 1
---

# Install Dragonfly Kubernetes Operator

Dragonfly Operator is a Kubernetes operator used to deploy and manage [Dragonfly](https://dragonflydb.io/) instances in your Kubernetes clusters.

The main features include:

- Automatic failover
- Scaling horizontally and vertically
- Custom configuration options

**Important**: Currently, Dragonfly Operator is in **Alpha**. You can find more information about Dragonfly
in the [official documentation](https://dragonflydb.io/docs/).
<!-- which is here? -->

## Prerequisites

- A working Kubernetes cluster (tested with Kubernetes 1.19+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed and configured to connect to your cluster

## Installation

Make sure your Kubernetes cluster is up and running. To install Dragonfly Operator, run:

```sh
# Install CRDs
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/crd.yaml
# Install the operator
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```

By default, the operator will be installed in the `dragonfly-operator-system` namespace.

## Usage

### Create a Dragonfly cluster

1. To create a sample Dragonfly cluster with a master and three replicas instances, run the this command:

    ```sh
    kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/config/samples/v1alpha1_dragonfly.yaml
    ```

1. To check the status of the cluster, run:

    ```sh
    kubectl describe dragonflies.dragonflydb.io dragonfly-sample
    ```

    The master instance of the service is available at `<dragonfly-name>.<namespace>.svc.cluster.local`, which you can use to connect to the cluster. As pods are added or removed, the service automatically updates to point to the new master.

#### Connect with `redis-cli`

To connect to the cluster using `redis-cli`, run:

```sh
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-sample.default
```

The command creates a temporary pod that runs the `redis-cli` and connects to the cluster. To run Redis commands, press `shift + R` and then enter the Redis commands. For example, to set and retrieve a key, you can run:

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

### Scale replica instances

To scale the number of replica instances up or down, edit the `spec.replicas` field in the Dragonfly instance. For example, to scale up to 5 replicas, run:

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"replicas":5}}'
```

### Pass custom Dragonfly arguments

To pass custom arguments to Dragonfly, edit the `spec.args` field in the Dragonfly instance. For example, to configure Dragonfly to a password, run:

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"args":["--requirepass=supersecret"]}}'
```

### Vertically scale the instance

To vertically scale the instance, edit the `spec.resources` field in the Dragonfly instance. For example, to increase the CPU limit to 2 cores, run:

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"resources":{"requests":{"memory":"1Gi"},"limits":{"memory":"2Gi"}}}}'
```
