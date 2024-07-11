---
description: "Learn Redis RENAMENX command to rename a key, only if the new key does not exist."
---

import PageTitle from '@site/src/components/PageTitle';

# RENAMENX

<PageTitle title="Redis RENAMENX Command (Documentation) | Dragonfly" />

## Syntax

    RENAMENX key newkey

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

Renames `key` to `newkey` if `newkey` does not yet exist.
It returns an error when `key` does not exist.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

- `1` if `key` was renamed to `newkey`.
- `0` if `newkey` already exists.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> SET myotherkey "World"
OK
dragonfly> RENAMENX mykey myotherkey
(integer) 0
dragonfly> GET myotherkey
"World"
```
