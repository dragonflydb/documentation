---
sidebar_position: 5
---

# High Availability with Dragonfly Operator

Dragonfly Operator is a Kubernetes operator that manages Dragonfly instances. It's available on [GitHub](https://github.com/dragonflydb/dragonfly-operator)
and can be installed on any Kubernetes cluster.

One of the main features of the Operator is out-of-the-box high availability. It allows you to run Dragonfly in a highly available configuration with minimal effort. By default, When you set the `replicas` field to a value greater than 1, the Operator will automatically configure Dragonfly to run in HA mode where
one instance is the master and the rest are replicas. As these pods go up and down, the Operator will automatically reconfigure Dragonfly to maintain the desired number of replicas with one master available at all times.

The application clients can continue using the same Dragonfly service, without any changes, and the Operator will automatically update the pod selectors to point to the right master.

Let's see how this works in practice.

## Installing the Operator

Follow the [installation instructions](../getting-started/kubernetes-operator.md#installation) to install the Operator on your Kubernetes cluster.

## Creating a Dragonfly instance

To create a sample Dragonfly instance, you can run the following command:

```sh
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/config/samples/v1alpha1_dragonfly.yaml
```

This will create a Dragonfly instance with 2 replicas. You can check the status of the instance by running

```sh
kubectl describe dragonflies.dragonflydb.io dragonfly-sample
```

A service of the form `<dragonfly-name>.<namespace>.svc.cluster.local` will be created, that selects the master instance. You can use this service to connect to the cluster. As pods are added/removed, the service will automatically update to point to the new master.

### Connecting with `redis-cli`

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

## High Availability

Let's see how the Operator maintains high availability in the face of failures.

Delete the master pod:

```sh
kubectl delete pod -l role=master
```

The Operator will automatically create a new master pod and update the service to point to the new master. You can check the status of the Dragonfly instance by running

```sh
kubectl describe dragonflies.dragonflydb.io dragonfly-sample
```

The data should also be preserved. You can check this by running

```sh
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-sample.default
If you don't see a command prompt, try pressing enter.
dragonfly-sample.default:6379> GET 1
"2"
dragonfly-sample.default:6379> exit
pod "redis-cli" deleted
```

## Conclusion

In this tutorial, we saw how to use the Dragonfly Operator to run Dragonfly in a highly available configuration. The Operator automatically manages the Dragonfly instances and ensures that the service is always available, even in the face of failures.
