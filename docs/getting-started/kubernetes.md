---
sidebar_position: 1
---

# Install on Kubernetes with Helm Chart

This guide describes how to deploy Dragonfly on a Kubernetes cluster using Helm (See [Install Helm](https://helm.sh/docs/intro/install/)).

## Prerequisites

- A Kubernetes cluster (see [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) or [Minikube](https://minikube.sigs.k8s.io/docs/start/) if you want to experiment locally).
- Select the Dragonfly version:
  - For the latest version, set:
    `VERSION=v{{DRAGONFLY_VERSION}}`
  - Choose a version from [here](https://github.com/dragonflydb/dragonfly/pkgs/container/dragonfly%2Fhelm%2Fdragonfly)

## Install a standalone master

Run this command:

`helm upgrade --install dragonfly oci://ghcr.io/dragonflydb/dragonfly/helm/dragonfly --version $VERSION`

## Install a standalone master with snapshot taken every minute

1. Add the following to the `myvals.yaml` values file (create a new file if it doesn't exist):

```yml "
storage:
  enabled: true
  requests: 128Mi # Set as desired

extraArgs:
  - --dbfilename=dump.rdb
  - --snapshot_cron=* * * * * # cron format

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

1. Run this command:
   `helm upgrade -f myvals.yaml --install dragonfly oci://ghcr.io/dragonflydb/dragonfly/helm/dragonfly --version $VERSION`

## Integrate with Kube-Prometheus Monitoring

If you have [Kube-Prometheus](https://github.com/prometheus-operator/kube-prometheus) installed in your cluster, you set it to monitor your Dragonfly deployment by enabling the `serviceMonitor` and `prometheusRule` in your values file. For example:

```yml "
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

## More Customization

For more customization please see the [Dragonfly Chart](https://github.com/dragonflydb/dragonfly/tree/main/contrib/charts/dragonfly)
