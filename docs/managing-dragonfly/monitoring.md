---
sidebar_position: 5
---

# Monitoring

By default, Dragonfly allows HTTP access via its main TCP port (i.e, `6379`) and it exposes Prometheus compatible metrics on `:6379/metrics`.

You can use our [public Grafana dashboard](https://grafana.com/grafana/dashboards/25167-dragonfly-cloud/) to monitor your Dragonfly instance.
Also check out this complete example of setting up a [Grafana Monitoring Stack with Dragonfly](https://github.com/dragonflydb/dragonfly/tree/main/tools/local/monitoring).

** :warning: **

If you're using kubernetes, Metrics are also available on admin port `9999`. You may encounter this error with port `6379`:

```
* Request completely sent off
* Received HTTP/0.9 when not allowed
* Closing connection
curl: (1) Received HTTP/0.9 when not allowed
```
