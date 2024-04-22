---
description:  Learn how to use Redis REPLICAOF command to convert a master instance into its replicas.
---

import PageTitle from '@site/src/components/PageTitle';

# REPLICAOF

<PageTitle title="Redis REPLICAOF Command (Documentation) | Dragonfly" />

## Syntax

    REPLICAOF host port

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

The `REPLICAOF` command can change the replication settings of a replica on the fly.

If a Dragonfly server is already acting as replica, the command `REPLICAOF NO ONE` will turn off the replication, turning the Dragonfly server into a MASTER.
In the proper form `REPLICAOF hostname port` will make the server a replica of another server listening at the specified hostname and port.

If a server is already a replica of some master, `REPLICAOF hostname port` will stop the replication against the old server and start the synchronization against the new one, discarding the old dataset.

The form `REPLICAOF NO ONE` will stop replication, turning the server into a MASTER, but will not discard the replication.
So, if the old master stops working, it is possible to turn the replica into a master and set the application to use this new master in read/write.
Later when the other Dragonfly server is fixed, it can be reconfigured to work as a replica.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings)

## Examples

```
dragonfly> REPLICAOF NO ONE
OK

dragonfly> REPLICAOF 127.0.0.1 6799
OK
```
## Flags
* **`masterauth`** - the credentials for accessing authenticated master server
