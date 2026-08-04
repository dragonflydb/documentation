---
description: "Monitor a Dragonfly instance's HTTP and Prometheus-compatible metrics endpoint, including replication metrics."
sidebar_position: 5
---

# Monitoring

By default, Dragonfly allows HTTP access through its main TCP port (i.e., `6379`) and exposes Prometheus-compatible metrics at `:6379/metrics`. These include metrics for connection memory and pipelines. Batch I/O counters are available through `INFO stats`, but are not currently exported by the Prometheus endpoint.

Check out this complete example of setting up a [Grafana Monitoring Stack with Dragonfly](https://github.com/dragonflydb/dragonfly/tree/main/tools/local/monitoring).

** :warning: **

If you're using kubernetes, Metrics are also available on admin port `9999`. You may encounter this error with port `6379`:

```
* Request completely sent off
* Received HTTP/0.9 when not allowed
* Closing connection
curl: (1) Received HTTP/0.9 when not allowed
```

## Replication Metrics

The `/metrics` endpoint also exposes replication information. These metrics include details about the replication role of the instance, connected replicas, replication backlog, and replication lag, allowing you to monitor the health and status of your Dragonfly replication setup via Prometheus.
