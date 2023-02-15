---
description: Sort the elements in a list, set or sorted set. Read-only variant of SORT.
---

# SORT_RO

## Syntax

    SORT_RO key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC | DESC] [ALPHA]

**Time complexity:** O(N+M*log(M)) where N is the number of elements in the list or set to sort, and M the number of returned elements. When the elements are not sorted, complexity is O(N).

Read-only variant of the `SORT` command. It is exactly like the original `SORT` but refuses the `STORE` option and can safely be used in read-only replicas.

Since the original `SORT` has a `STORE` option it is technically flagged as a writing command in the Redis command table. For this reason read-only replicas in a Redis Cluster will redirect it to the master instance even if the connection is in read-only mode (see the `READONLY` command of Redis Cluster).

The `SORT_RO` variant was introduced in order to allow `SORT` behavior in read-only replicas without breaking compatibility on command flags.

See original `SORT` for more details.

## Examples

```
SORT_RO mylist BY weight_*->fieldname GET object_*->fieldname
```

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): a list of sorted elements.
