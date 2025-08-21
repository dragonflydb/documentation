---
description: "Explore the Redis TYPE command for finding a key's data type."
---

import PageTitle from '@site/src/components/PageTitle';

# TYPE

<PageTitle title="Redis TYPE Command (Documentation) | Dragonfly" />

## Syntax

    TYPE key

**Time complexity:** O(1)

**ACL categories:** @keyspace, @read, @fast

Returns the string representation of the type of the value stored at `key`.
The different types that can be returned are: `string`, `list`, `set`, `zset`,
`hash`, `stream` and `ReJSON-RL`.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): type of `key`, or `none` when `key` does not exist.

## Examples

```shell
dragonfly> SET key1 "value"
OK
dragonfly> LPUSH key2 "value"
(integer) 1
dragonfly> SADD key3 "value"
(integer) 1
dragonfly> TYPE key1
"string"
dragonfly> TYPE key2
"list"
dragonfly> TYPE key3
"set"
```
