---
description: "Discover how to use Redis SORT_RO command for read-only sorting of elements in list, set or sorted sets."
---

import PageTitle from '@site/src/components/PageTitle';

# SORT_RO

<PageTitle title="Redis SORT_RO Command (Documentation) | Dragonfly" />

## Syntax

    SORT_RO key [LIMIT offset count] [ASC | DESC] [ALPHA]

**Time complexity:** O(N+M\*log(M)) where N is the number of elements in the list or set to sort, and M the number of returned elements. When the elements are not sorted, complexity is O(N).

**ACL categories:** @read, @set, @sortedset, @list, @slow

Read-only variant of the [SORT](./sort) command. It is exactly like the original [SORT](./sort) command but refuses the `STORE` option and can safely be used in read-only replicas.

Since the original [SORT](./sort) has a `STORE` option it is technically flagged as a writing command in the Redis command table. For this reason read-only replicas in a Redis Cluster will redirect it to the master instance even if the connection is in read-only mode.

The `SORT_RO` variant was introduced in order to allow [SORT](./sort) behavior in read-only replicas without breaking compatibility on command flags.

See [SORT](./sort) for more details about the command and its options.

## Dragonfly Support

Dragonfly currently supports the following options for `SORT_RO`:
- `ASC` / `DESC` - Sort order
- `ALPHA` - Lexicographical sorting
- `LIMIT offset count` - Limit results

The following options are **not yet supported**:
- `BY pattern` - Sort by external keys
- `GET pattern` - Retrieve external keys

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): list of sorted elements.

## Examples

```shell
dragonfly> LPUSH mylist 3 1 2
(integer) 3

dragonfly> SORT_RO mylist
1) "1"
2) "2"
3) "3"

dragonfly> SORT_RO mylist DESC
1) "3"
2) "2"
3) "1"

dragonfly> SORT_RO mylist ALPHA
1) "1"
2) "2"
3) "3"

dragonfly> SORT_RO mylist LIMIT 0 2
1) "1"
2) "2"
```
