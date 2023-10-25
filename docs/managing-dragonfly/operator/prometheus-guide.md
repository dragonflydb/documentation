---
sidebar_position: 4
---

# Integrate Prometheus with the Dragonfly Operator

This guide provides step-by-step instructions to set up Prometheus with the Dragonfly
Operator. In this guide, you'll use the [Promethues Operator](https://github.com/prometheus-operator/prometheus-operator)
and PodMonitor to manage Prometheus resources.

## Prerequisites

- A Kubernetes cluster with [Dragonfly installed](./installation.md)

## Install Prometheus Operator

First make sure you have all the Prometheus CRDs installed in your cluster. Run the
below commands to install the Prometheus Operator.

```
LATEST=$(curl -s https://api.github.com/repos/prometheus-operator/prometheus-operator/releases/latest | jq -cr .tag_name)
curl -sL https://github.com/prometheus-operator/prometheus-operator/releases/download/${LATEST}/bundle.yaml | kubectl create -f -
```

## Create the PodMonitor Resource

PodMonitors allow Prometheus to monitor specific pods that has the target labels. It
is the easiest way to monitor Dragonfly pods. You can either create your own
PodMonitor config file or use our sample [podMonitor.yaml](https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/podMonitor.yaml)
file to create a PodMonitor object.

```
kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/podMonitor.yaml
```

Note you must use `app: <dragonfly-name>` as a selector label in the PodMonitor to
target the correct Dragonfly instances. The label value is the name of your Dragonfly
resource (in this case, `dragonfly-sample`).

The Dragonfly pod exposes a port named `admin` which you can use as the endpoint in
PodMonitor.

## Create Promethues Resources

Now you have installed the operator and PodMonitor, it is time to create the
`prometheus` resources. If you have RBAC enabled, create the necessary
`serviceaccount`, `clusterrole` and `clusterrolebinding` resources first.

```
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/promServiceAccount.yaml
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/promClusterRole.yaml
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/promClusterBinding.yaml
```

This will allow Prometheus to scrape data from Dragonfly resources. Run the below
command to create the Prometheus object. It will create a pod named `prometheus-prometheus-0`.

```
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/prometheus-config.yaml
```

You can also create a service that points to the Prometheus pod.

```
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/prometheus-service.yaml
```

Run `kubectl get all` to check if all the resources have successfully been created.

```
$ kubectl get all
NAME                                       READY   STATUS    RESTARTS         AGE
pod/dragonfly-sample-0                     1/1     Running   4 (3h50m ago)    12d
pod/dragonfly-sample-1                     1/1     Running   4 (3h50m ago)    12d
pod/prometheus-operator-744c6bb8f9-vnxw4   1/1     Running   16 (3h49m ago)   19d
pod/prometheus-prometheus-0                2/2     Running   6 (3h50m ago)    11d

NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/dragonfly-sample      ClusterIP   10.96.2.149     <none>        6379/TCP   12d
service/kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP    45d
service/prometheus-operated   ClusterIP   None            <none>        9090/TCP   11d
service/prometheus-operator   ClusterIP   None            <none>        8080/TCP   19d
service/prometheus-svc        ClusterIP   10.96.8.22      <none>        9090/TCP   11d

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/prometheus-operator   1/1     1            1           19d

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/prometheus-operator-744c6bb8f9   1         1         1       19d

NAME                                     READY   AGE
statefulset.apps/dragonfly-sample        2/2     12d
statefulset.apps/prometheus-prometheus   1/1     11d
```

## Access Prometheus UI

Prometheus has a beautiful UI that you can use to query certain metrics. Use the
`port-forward` command to either directly expose the Prometheus pod (port 9090) or
expose the Prometheus service.

```
kubectl port-forward prometheus-prometheus-0 9090:9090
```
Now go to `localhost:9090`. Congratulations! You just integrated Prometheus with
Dragonfly!
