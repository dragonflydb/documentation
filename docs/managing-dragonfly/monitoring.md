---
sidebar_position: 5
---

# Monitoring

## Metrics via the Main TCP Port

By default, Dragonfly allows HTTP access via its main TCP port (`6379` by default), and it exposes Prometheus-compatible metrics at `:6379/metrics`.

Refer to this complete example of setting up a [Grafana Monitoring Stack with Dragonfly](https://github.com/dragonflydb/dragonfly/tree/main/tools/local/monitoring).

## Dragonfly Kubernetes Operator

If you're using the [Dragonfly Kubernetes Operator](operator/installation.md), metrics are also available on admin port `9999` internally inside the Kubernetes cluster.

You may encounter this error with port `6379`:

```shell
$> curl localhost:6379/metrics --verbose
# * Received HTTP/0.9 when not allowed
# * Closing connection
# curl: (1) Received HTTP/0.9 when not allowed
```

However, you can still access the metrics at `:9999/metrics` without any issues:

```shell
# Port-forward the pod's admin port to your local machine.
$> kubectl port-forward dragonfly-pod-1 '9999:9999'

# Now you can access the metrics via the forwarded port.
$> curl localhost:9999/metrics
```
