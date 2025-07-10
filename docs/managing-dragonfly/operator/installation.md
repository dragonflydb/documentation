---
sidebar_position: 1
---

# Install Dragonfly Kubernetes Operator

Dragonfly Operator is a Kubernetes operator used to deploy and manage [Dragonfly](https://dragonflydb.io/) instances in your Kubernetes clusters.

The main features include:

- Automatic Failover
- Scaling Horizontally and Vertically (with Custom Rollout Strategy)
- Custom Configuration Options
- Authentication and Server TLS
- Snapshots to Persistent Volume Claims (PVCs) and S3-Compatible Cloud Storage
- Monitoring with Prometheus and Grafana

## Prerequisites

- A working Kubernetes cluster (tested with Kubernetes 1.19+).
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed and configured to connect to your Kubernetes cluster.

## Installation

Make sure your Kubernetes cluster is up and running. To install Dragonfly Operator, run the following command:

```shell
# Install the Dragonfly Kubernetes Operator.
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```

By default, the operator will be installed in the `dragonfly-operator-system` namespace.

## Usage

### Create a Dragonfly instance with replicas

To set up a sample Dragonfly topology with a primary (master) and optional replicas (slaves), create a YAML file:

```yaml
# dragonfly-sample.yaml
apiVersion: dragonflydb.io/v1alpha1
kind: Dragonfly
metadata:
  labels:
    app.kubernetes.io/name: dragonfly
    app.kubernetes.io/instance: dragonfly-sample
    app.kubernetes.io/part-of: dragonfly-operator
    app.kubernetes.io/managed-by: kustomize
    app.kubernetes.io/created-by: dragonfly-operator
  name: dragonfly-sample
spec:
  replicas: 2
  resources:
    requests:
      cpu: 500m
      memory: 500Mi
    limits:
      cpu: 600m
      memory: 750Mi
```

And then run the following command:

```shell
kubectl apply -f dragonfly-sample.yaml
```

**Important Note:**
When using the Dragonfly Kubernetes Operator, the `replicas` configuration adheres to Kubernetes' standard semantics, specifying the number of instances to run.
However, since Dragonfly is a stateful data store, the interpretation differs, as it relates to a high-availability setup.
For example:

- Setting `replicas=1` creates 1 primary instance of Dragonfly only.
- Setting `replicas=2` creates 1 primary and 1 replica of Dragonfly.
- Setting `replicas=3` creates 1 primary and 2 replicas of Dragonfly, and so on.
- There is always only 1 primary Dragonfly instance.

To check the status of the instance, run the following command:

```shell
kubectl describe dragonflies.dragonflydb.io dragonfly-sample
```

Connect to the primary instance of the service at: `<dragonfly-name>.<namespace>.svc.cluster.local`.
As pods are added or removed, the service automatically updates to point to the new primary.

### Connect with `redis-cli`

To connect to the instance using `redis-cli`, run the following command:

```shell
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-sample.default
```

The command creates a temporary pod that runs the `redis-cli` and connects to the instance.
For example, to set and retrieve a key, run the following commands:

```shell
# If you don't see a command prompt, try pressing enter.
dragonfly-sample.default:6379$> GET my_key
(nil)

dragonfly-sample.default:6379$> SET my_key my_val
OK

dragonfly-sample.default:6379$> GET my_key
"my_val"

dragonfly-sample.default:6379$> QUIT
OK
```

### Change the number of replica instances

To change the number of replica instances, edit the `spec.replicas` field.
For example, to scale up to 1 primary with 4 replica instances of Dragonfly, run the following command:

```shell
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"replicas":5}}'
```

### Pass custom Dragonfly arguments

To pass custom arguments ([server configuration flags](../flags.md))
to Dragonfly, edit the `spec.args` field.
For example, to configure Dragonfly to require a password, run the following command:

```shell
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"args":["--requirepass=supersecret"]}}'
```

### Vertically scale the instances

To vertically scale the instances, edit the `spec.resources` field.
For example, to increase the CPU requests to 2 cores, run the following command:

```shell
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"resources":{"requests":{"cpu":"2"}}}}'
```

To understand how to configure high availability,
please refer to the [related section](/docs/managing-dragonfly/high-availability.md#high-availability-with-dragonfly-operator).
