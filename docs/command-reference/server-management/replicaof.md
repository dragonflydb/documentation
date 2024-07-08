---
description: Learn how to use Redis REPLICAOF command to convert a master instance into its replicas.
---

import PageTitle from '@site/src/components/PageTitle';

# REPLICAOF

<PageTitle title="Redis REPLICAOF Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `REPLICAOF` command in Redis is used to make the current server a replica (slave) of another instance or to promote it back to a master. This command is particularly useful in scenarios where you need to configure replication for high availability, load balancing, or read scalability.

## Syntax

```
REPLICAOF host port
```

## Parameter Explanations

- **host**: The hostname or IP address of the master instance you want this server to replicate.
- **port**: The port number on which the master instance is accepting connections.

Setting `REPLICAOF no one` will demote the instance from being a replica and return it to standalone mode.

## Return Values

This command returns `OK` if the operation was successful. If the server is already a replica of the specified master, it will also return `OK`.

Example outputs:

- `OK`: When the replica configuration is successfully applied.
- `(error) ERR`: If there's an error applying the replication.

## Code Examples

```cli
dragonfly> REPLICAOF 127.0.0.1 6379
OK
dragonfly> REPLICAOF no one
OK
```

## Common Mistakes

- **Incorrect Host/Port**: Specifying a wrong host or port will lead to connection failures.
- **Forget to Demote**: Not using `REPLICAOF no one` when promoting a replica back to a master can lead to unintended replication behavior.

## FAQs

### What happens to the data on the slave when you run REPLICAOF?

When you run `REPLICAOF`, the data on the slave will be overwritten by the data from the master during synchronization.

### Can you use REPLICAOF to switch masters dynamically?

Yes, you can use `REPLICAOF` to change the master that a replica server is following without restarting either the master or the replica.

## Best Practices

- **Monitor Replication Lag**: Regularly monitor replication lag to ensure your replicas are up-to-date with the master.
- **Network Stability**: Ensure a stable network connection between master and replicas to avoid frequent disconnections and data inconsistencies.
