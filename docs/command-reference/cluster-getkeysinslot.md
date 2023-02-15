---
description: Return local key names in the specified hash slot
---

# CLUSTER GETKEYSINSLOT

## Syntax

    CLUSTER GETKEYSINSLOT slot count

**Time complexity:** O(N) where N is the number of requested keys

The command returns an array of keys names stored in the contacted node and
hashing to the specified hash slot. The maximum number of keys to return
is specified via the `count` argument, so that it is possible for the user
of this API to batch-processing keys.

The main usage of this command is during rehashing of cluster slots from one
node to another. The way the rehashing is performed is exposed in the Redis
Cluster specification, or in a more simple to digest form, as an appendix
of the `CLUSTER SETSLOT` command documentation.

```
> CLUSTER GETKEYSINSLOT 7000 3
1) "key_39015"
2) "key_89793"
3) "key_92937"
```

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): From 0 to *count* key names in a Redis array reply.
