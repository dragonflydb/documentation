---
sidebar_position: 4
---

# Integrate Prometheus with Dragonfly operator

This guide provides a step-by-step instruction to set up Prometheus to monitor
Dragonfly pods. In this guide, you're going to use [Promethues Operator](https://github.com/prometheus-operator/prometheus-operator) along with PodMonitor.

## Prerequisites

- A kubernetes cluster with [Dragonfly installed](./installation.md)

## Install Prometheus Operator
First make sure you have all the prometheus crds installed in your cluster. Run the
below commands to install the Prometheus Operator.

```
LATEST=$(curl -s https://api.github.com/repos/prometheus-operator/prometheus-operator/releases/latest | jq -cr .tag_name)
curl -sL https://github.com/prometheus-operator/prometheus-operator/releases/download/${LATEST}/bundle.yaml | kubectl create -f -
```

## Create the PodMonitor Resource

PodMonitors allow Prometheus to monitor specific pods that has the target labels. It
is the easiest way to monitor Dragonfly pods. Either create your own PodMonitor
config file or use our sample [podMonitor.yaml](https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/podMonitor.yaml) file to create a PodMonitor
object.

```
kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/podMonitor.yaml
```

Note that you must use `app: <dragonfly-name>` label as selector label in the
PodMonitor in order to target the correct dragonfly instances. The value of `app`
label is the name of your dragonfly resource name (in this case, `dragonfly-sample`).

Dragonfly resources expose a port named `admin` and you can use it as the endpoint in PodMonitor.

## Create Promethues Resources

Now that you have installed the operator and pod-monitor, it is time to create
`prometheus` resources. If you have RBAC enabled, create necessary `serviceaccount`,
`clusterrole` and `clusterrolebinding` resources first.

```
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/promServiceAccount.yaml
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/promClusterRole.yaml
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/promClusterBinding.yaml
```

This will allow prometheus to scrape data from dragonfly resources. Run the below
command to create a Prometheus pod named `prometheus-prometheus-0`.

```
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/prometheus-config.yaml
```

You can also create a service that points to the prometheus pod.

```
$ kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/prometheus-service.yaml
```

You can run `kubectl get all` to check if all the resources has successfully
created.

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

Prometheus has a beautiful UI that you can use to query certain metrics. You can
use `port-forward` command to either directly expose the prometheus pod 9090 port
or expose the prometheus service.

```
kubectl port-forward prometheus-prometheus-0 9090:9090
```
Now go to `localhost:9090`. Congratulations! You just integrated Prometheus with
Dragonfly!
