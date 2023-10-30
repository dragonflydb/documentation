---
sidebar_position: 5
---

# Integrate Grafana with Dragonfly operator

In this guide, we are going to see how we can setup Grafana dashboard to monitor
Dragonfly pods in kubernetes cluster.

## Prerequisites

- A kubernetes cluster with [Dragonfly installed](./installation.md)
- Prometheus setup in the cluster. See [Prometheus integration guide](./prometheus-guide.md)
- You have [Helm](https://helm.sh/docs/intro/install/) installed.

If you already have Grafana instance in your cluster, use [grafana-dashboard.json](https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/grafana-dashboard.json)
to import the dashboard.


## Install Grafana helm chart

We'll be using [grafana helm chart](https://github.com/grafana/helm-charts) to setup
Grafana. So make sure you have [Helm](https://helm.sh/docs/intro/install/) installed.

```
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana-ui grafana/grafana
```

Once you run the command, `grafana` will create all the necessary resources to setup
grafana. Run the below command to check if all resources are created successfully.

```
$ kubectl get all
NAME                                       READY   STATUS    RESTARTS        AGE
pod/dragonfly-sample-0                     1/1     Running   1 (171m ago)    23h
pod/dragonfly-sample-1                     1/1     Running   1 (171m ago)    23h
pod/grafana-ui-785f79fb65-rmk52            1/1     Running   1 (171m ago)    23h
pod/prometheus-operator-744c6bb8f9-vnxw4   1/1     Running   10 (170m ago)   8d
pod/prometheus-prometheus-0                2/2     Running   0               167m

NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/dragonfly-sample      ClusterIP   10.96.2.149     <none>        6379/TCP   23h
service/grafana-ui            ClusterIP   10.96.146.235   <none>        80/TCP     23h
service/kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP    33d
service/prometheus-operated   ClusterIP   None            <none>        9090/TCP   167m
service/prometheus-operator   ClusterIP   None            <none>        8080/TCP   8d

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/grafana-ui            1/1     1            1           23h
deployment.apps/prometheus-operator   1/1     1            1           8d

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/grafana-ui-785f79fb65            1         1         1       23h
replicaset.apps/prometheus-operator-744c6bb8f9   1         1         1       8d

NAME                                     READY   AGE
statefulset.apps/dragonfly-sample        2/2     23h
statefulset.apps/prometheus-prometheus   1/1     167m
```

## Create Prometheus Service

Create a prometheus Service to let Grafana access prometheus through it. If you already
have a Prometheus Service object, move to the next step.

```
kubectl apply -f https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/prometheus-service.yaml
```

Note that it is required to use `prometheus: prometheus` label as selector (if no label is given to the existing Prometheus object). The prometheus operator exposes
a port named `web`, so you can use this port as targetPort in the service.

## Create Grafana dashboard

The helm chart also creates a `grafana-ui` service which you can use to port-forward
the grafana port.

```
kubectl port-forward services/grafana-ui 3000:80
```

Now go to `localhost:3000`. You will see a grafana dashboard running in the localhost.
 add a Prometheus data source. Use `http://prometheus-svc:9090` as the datasource url. After that, import [grafana-dashboard.json](https://github.com/dragonflydb/dragonfly-operator/blob/main/monitoring/grafana-dashboard.json) to the dashboard.