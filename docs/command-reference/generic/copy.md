---
description: "Learn how to use Redis COPY command to copy a key."
---

import PageTitle from '@site/src/components/PageTitle';

# COPY

<PageTitle title="Redis COPY Command (Documentation) | Dragonfly" />

## Syntax

    COPY source destination [REPLACE]

**Time complexity:** O(N) worst case for collections, where N is the number of nested items. O(1) for string values.

**ACL categories:** @keyspace, @write, @slow

Copies the value at `source` key to the `destination` key.
The `REPLACE` option removes an existing key before copying.

## Return

- [Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): `1` if the `source` was copied.
- [Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): `0` if the `source` was not copied when `destination` already exists.

## Examples

```shell
dragonfly> SET key1 "Hello"
OK

# Since 'key2' does not exist, the value of 'key1' is copied.
dragonfly> COPY key1 key2
(integer) 1
dragonfly> GET key2
"Hello"

# Let's change the value of 'key1'.
dragonfly> SET key1 "World"
OK

# Since 'key2' already exists, the value of 'key1' is not copied.
dragonfly> COPY key1 key2
(integer) 0
dragonfly> GET key2
"Hello"

# With the 'REPLACE' option, the command removes 'key2' before copying the value of 'key1' to it.
dragonfly> COPY key1 key2 REPLACE
(integer) 1
dragonfly> GET key2
"World"
```
