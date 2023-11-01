---
sidebar_position: 2
---

# Dragonfly Configuration

Dragonfly Operator uses a dedicated Dragonfly CRD to create and manage Dragonfly
resources. The CRD allows various configurations to define the behaviour of dragonfly
controller and the dragonfly pods. Below is the table of Dragonfly CRD fields.

| fields | type | Description |
| ------ | ---- | ----------- |
| `affinity` | [Affinity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#affinity-v1-core) | Dragonfly pod affinity (Optional)<br/><pre>spec:<br/>  affinity: <br/>    nodeaffinity:<br/>      ...</pre> You can learn more about affinity [here](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity).|
| `replicas` | int | The total number of Dragonfly instances including the master. |
| `image` | string | The dragonfly image to use. Default is `docker.dragonflydb.io/dragonflydb/dragonfly:v1.10.0` |
| `args` | []string | (Optional) Dragonfly container args to pass to the container. Refer to the Dragonfly documentation for the list of supported args. Example - <br/><pre>spec:<br/>  args:<br/>   - "--cluster_mode=emulated"</pre> |
| `annotations` | object | (Optional) Annotations to add to the Dragonfly pods. See [Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) to know more about annotations. |
| `env` | array | Environmental Variables to add to Dragonfly pods. Example - <br/><pre>spec:<br/>  env:<br/>   - name: DEBUG<br/>     value: true</pre>|
| `resources` | [ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#resourcerequirements-v1-core) | (Optional) Dragonfly container resource limits. Any container limit can be specified.|
| `tolerations` | \[][Toleration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#toleration-v1-core) | (Optional) Dragonfly pod tolerations. See [k8s doc](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) to know more about tolerations |
| `serviceAccountName` | string | (Optional) Dragonfly pod service account name |
| `serviceSpec.type` | string | (Optional) Dragonfly Service type |
| `serviceSpec.annotations` | object | (Optional) Dragonfly Service Annotations |
| `authentication.passwordFromSecret` | [SecretKeySelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#secretkeyselector-v1-core) | (Optional) Dragonfly Password from Secret as a reference to a specific key. Example - <pre>spec:<br/>  authentication:<br/>    passwordFromSecret:<br/>      name: dragonfly-auth-secret<br/>      key: password<br/></pre> |
| `authentication.clientCaCertSecret` | [SecretReference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#secretreference-v1-core) | (Optional) If specified, the Dragonfly instance will check if the client certificate is signed by one of this CA. Server TLS must be enabled for this. Multiple CAs can be specified with various key names. Example - <pre>spec:<br/>  authentication:<br/>    clientCaCertSecret:<br/>      name: dragonfly-client-ca<br/></pre> |
| `tlsSecretRef` | [SecretReference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#secretreference-v1-core) | (Optional) Dragonfly TLS secret to used for TLS Connections to Dragonfly. Dragonfly instance  must have access to this secret and be in the same namespace. Example - <pre>spec:<br/>  tlsSecretRef:<br/>    name: dragonfly-secret</pre><br/>|
| `snapshot.cron` | string | (Optional) Dragonfly snapshot schedule |
| `snapshot.persistentVolumeClaimSpec` | [PersistentVolumeClaimSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#persistentvolumeclaimspec-v1-core) | (Optional) Dragonfly PVC spec |