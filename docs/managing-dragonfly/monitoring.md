---
sidebar_position: 5
---

# Monitoring

By default, Dragonfly allows HTTP access via its main TCP port (i.e, `6379`) and it exposes Prometheus compatible metrics on `:6379/metrics`.

Check out this complete example of setting up a [Grafana Monitoring Stack with Dragonfly](https://github.com/dragonflydb/dragonfly/tree/main/tools/local/monitoring).
