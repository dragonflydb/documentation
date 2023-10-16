---
sidebar_position: 2
---

# Snapshots through PVC

This guide provides step-by-step instructions for setting up Dragonfly with snapshots through PVC. [Dragonfly already supports snapshots](https://www.dragonflydb.io/docs/managing-dragonfly/backups), which allows you to create a snapshot of your database at any point in time and restore it later. With this PVC integration, you can now store your snapshots in [persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)  and get them automatically restored when your Dragonfly pods get restarted or rescheduled across nodes. This is possible as a specific PVC is attached to each Dragonfly statefulset and the snapshot is stored in that PVC. The persistent volume can be backed by any storage provider that Kubernetes supports.

While this feature can help you recover from failures, It is not a replacement for Replication. You should still use replication if you want to
maintain high availability.

## Prerequisites

- A Kubernetes cluster with [Dragonfly installed](./installation.md).
- Relevant [storage provider](https://kubernetes.io/docs/concepts/storage/storage-classes/) installed and available in the cluster.

## Deploying Dragonfly with Snapshots through PVC

Apply a Dragonfly manifest with PVC enabled on the default storage class:

```bash
kubectl apply -f - <<EOF
apiVersion: dragonflydb.io/v1alpha1
kind: Dragonfly
metadata:
  name: dragonfly-pvc
spec:
  replicas: 1
  snapshot:
    cron: "*/5 * * * *"
    persistentVolumeClaimSpec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 2Gi
EOF
```

This will create a Dragonfly statefulset with the given PVC spec. The `persistentVolumeClaimSpec` field is the same as the one used in [Kubernetes PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) and can be used to configure the PVC as per your requirements.

Wait for the Dragonfly instance to be ready:

```bash
kubectl describe dragonflies.dragonflydb.io dragonfly-pvc
```

## Testing

Connect to the Dragonfly instance and add some data:

```bash
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-pvc.default SET foo bar
If you don't see a command prompt, try pressing enter.
pod "redis-cli" deleted
```

Delete the Dragonfly pod:

```bash
kubectl delete pod dragonfly-pvc-0
```

Wait for the pod to be recreated:

```bash
kubectl get pods -w
```

Connect to the Dragonfly instance, and check if the data is still there:

```bash
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-pvc.default GET foo
"bar"
pod "redis-cli" deleted
```

You should see the value `bar` for the key `foo`. This means that the data was restored from the snapshot that was stored in the PVC.
