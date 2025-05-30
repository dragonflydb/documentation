---
sidebar_position: 1
---

import PageTitle from '@site/src/components/PageTitle';

# Install Dragonfly Kubernetes Operator

<PageTitle title="Getting Started with Kubernetes Operator | Dragonfly" />

Dragonfly Operator is a Kubernetes operator used to deploy and manage [Dragonfly](https://dragonflydb.io/) instances in your Kubernetes clusters.

The main features include:

- Automatic Failover
- Scaling Horizontally and Vertically (with Custom Rollout Strategy)
- Custom Configuration Options
- Authentication and Server TLS
- Snapshots to Persistent Volume Claims (PVCs) and S3-Compatible Cloud Storage
- Monitoring with Prometheus and Grafana

## Prerequisites

- A working Kubernetes cluster (tested with Kubernetes 1.19+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed and configured to connect to your cluster

## Installation

Make sure your Kubernetes cluster is up and running. To install Dragonfly Operator, run:

```sh
# Install the CRD and Operator
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```

By default, the operator will be installed in the `dragonfly-operator-system` namespace.

## Usage

### Create a Dragonfly instance with replicas

1. To create a sample Dragonfly instance with a master and three replicas, run the this command:

    ```sh
    kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/config/samples/v1alpha1_dragonfly.yaml
    ```

2. To check the status of the instance, run:

    ```sh
    kubectl describe dragonflies.dragonflydb.io dragonfly-sample
    ```

3. Connect to the master instance of the service at:    
    `<dragonfly-name>.<namespace>.svc.cluster.local`.
    
    As pods are added or removed, the service automatically updates to point to the new master.

#### Connect with `redis-cli`

To connect to the instance using `redis-cli`, run:

```sh
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-sample.default
```

The command creates a temporary pod that runs the `redis-cli` and connects to the instance. To run Redis commands, press `shift + R` and then enter the Redis commands. For example, to set and retrieve a key, you can run:

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

### Change the number of replica instances

To change the number of replica instances, edit the `spec.replicas` field in the Dragonfly instance. For example, to scale up to 5 replicas run:

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"replicas":5}}'
```

### Pass custom Dragonfly arguments

To pass custom arguments to Dragonfly, edit the `spec.args` field in the Dragonfly instance. For example, to configure Dragonfly to require a password run:

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"args":["--requirepass=supersecret"]}}'
```

### Vertically scale the instance

To vertically scale the instance, edit the `spec.resources` field in the Dragonfly instance. For example, to increase the CPU requests to 2 cores run:

```sh
kubectl patch dragonfly dragonfly-sample --type merge -p '{"spec":{"resources":{"requests":{"cpu":"2"}}}}'
```

To understand how to configure High Availability, please refer to the [High Availability](/docs/managing-dragonfly/high-availability.md#high-availability-with-dragonfly-operator) section.
