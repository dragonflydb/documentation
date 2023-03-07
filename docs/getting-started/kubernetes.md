---
sidebar_position: 1
---

# Install with Kubernetes

## Prerequisites

- This manual uses Helm to deploy Dragonfly on a Kuberenetes cluster. See [Install Helm](https://helm.sh/docs/intro/install/)
- A Kuberenetes cluster (See [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) or [Minikube](https://minikube.sigs.k8s.io/docs/start/) if you want to experiment locally)
- For latest version set `VERSION=v$VERSION`
- Or pick a version from [here](https://github.com/dragonflydb/dragonfly/pkgs/container/dragonfly%2Fhelm%2Fdragonfly)

## Install a standalone master

`helm upgrade --install dragonfly oci://ghcr.io/dragonflydb/dragonfly/helm/dragonfly --version v{{DRAGONFLY_VERSION}}`

## Install a standalone master with snapshot taken every minute

Create or add to your myvals.yaml values file

```yml "
storage:
  enabled: true
  requests: 128Mi # Set as desired

extraArgs:
  - --dbfilename=dump.rdb
  - --save_schedule=*:* # HH:MM glob format

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

`helm upgrade -f myvals.yaml --install dragonfly oci://ghcr.io/dragonflydb/dragonfly/helm/dragonfly --version {{DRAGONFLY_VERSION}}`

## Integrate with Kube-Prometheus Monitoring

If you have [Kube-Prometheus](https://github.com/prometheus-operator/kube-prometheus) installed in your cluster, you can have it monitor your dragonfly deployment by enbaling the `serviceMonitor` and `prometheusRule` in your values file. See an example below.

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
