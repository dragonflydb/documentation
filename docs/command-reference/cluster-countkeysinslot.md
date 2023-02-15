---
description: Return the number of local keys in the specified hash slot
---

# CLUSTER COUNTKEYSINSLOT

## Syntax

    CLUSTER COUNTKEYSINSLOT slot

**Time complexity:** O(1)

Returns the number of keys in the specified Redis Cluster hash slot. The
command only queries the local data set, so contacting a node
that is not serving the specified hash slot will always result in a count of
zero being returned.

```
> CLUSTER COUNTKEYSINSLOT 7000
(integer) 50341
```

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): The number of keys in the specified hash slot, or an error if the hash slot is invalid.
