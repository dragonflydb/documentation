---
sidebar_position: 1
---

import PageTitle from '@site/src/components/PageTitle';

# Install on Kubernetes with Helm Chart

<PageTitle title="Getting Started with Helm | Dragonfly" />

This guide describes how to deploy Dragonfly on a Kubernetes cluster using Helm.
Before you begin, please ensure that [Helm is installed](https://helm.sh/docs/intro/install/) properly.

## Prerequisites

- A running Kubernetes cluster (see [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) or [Minikube](https://minikube.sigs.k8s.io/docs/start/) if you want to experiment locally).
- Select the Dragonfly version:
  - For the latest version, set `VERSION=v{{DRAGONFLY_VERSION}}` as an environment variable, which will be used later.
  - Choose from [here](https://github.com/dragonflydb/dragonfly/releases) if you need a specific version.

For full control and customization, please check out
the [complete list of configuration values](https://github.com/dragonflydb/dragonfly/tree/main/contrib/charts/dragonfly) you can use.
Now, let's see a couple of examples of deploying Dragonfly using Helm below.

## Standalone Instance

Run the following command to deploy a standalone primary Dragonfly instance:

```bash
helm upgrade \
    --install dragonfly oci://ghcr.io/dragonflydb/dragonfly/helm/dragonfly \
    --version $VERSION
```

## Standalone Instance with Snapshotting

Add the following to the [values file](https://helm.sh/docs/chart_template_guide/values_files/) (create a new values file if it doesn't exist):

```yml
storage:
  enabled: true
  requests: 128Mi # Set a desired volume size for PVC.

extraArgs:
  - --dbfilename=my-dump-{timestamp} # Only the filename without any file extensions.
  - --snapshot_cron=* * * * *        # Set a valid cron schedule.

podSecurityContext:
  fsGroup: 2000

securityContext:
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
```

Run the following command to deploy a Dragonfly instance with the configurations above:

```bash
# Make sure to use the correct values file.
helm upgrade -f values.yaml \
    --install dragonfly oci://ghcr.io/dragonflydb/dragonfly/helm/dragonfly \
    --version $VERSION
```

## Monitoring with Kube-Prometheus

If you have [Kube-Prometheus](https://github.com/prometheus-operator/kube-prometheus) installed in your cluster,
you can set it to monitor your Dragonfly deployment by enabling the `serviceMonitor` and `prometheusRule` in your values file.
For example:

```yml
serviceMonitor:
  enabled: true

prometheusRule:
  enabled: true
  spec:
    - alert: DragonflyMissing
      expr: absent(dragonfly_uptime_in_seconds) == 1
      for: 0m
      labels:
        severity: critical
      annotations:
        summary: Dragonfly is missing
        description: "Dragonfly is missing"
```
