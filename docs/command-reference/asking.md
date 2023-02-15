---
description: Sent by cluster clients after an -ASK redirect
---

# ASKING

## Syntax

    ASKING 

**Time complexity:** O(1)

When a cluster client receives an `-ASK` redirect, the `ASKING` command is sent to the target node followed by the command which was redirected.
This is normally done automatically by cluster clients.

If an `-ASK` redirect is received during a transaction, only one ASKING command needs to be sent to the target node before sending the complete transaction to the target node.

See [ASK redirection in the Redis Cluster Specification](https://redis.io/topics/cluster-spec#ask-redirection) for details.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK`.
