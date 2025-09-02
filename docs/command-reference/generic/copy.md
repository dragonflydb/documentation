---
description: "Learn how to use Redis COPY command to copy a key."
---

import PageTitle from '@site/src/components/PageTitle';

# COPY

<PageTitle title="Redis COPY Command (Documentation) | Dragonfly" />

## Syntax

    COPY src dest [DB destination] [REPLACE]

**Time complexity:** O(N) for collections where N is the number of items. O(1) for strings.

**ACL categories:** @keyspace, @write, @slow

Copies the value at `source` key to the `destination` key. The `DB` option allows specifying an alternative database index. The `REPLACE` option removes an existing key before copying.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): 1 if the source was copied.
[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): 0 if the source was copied when destination already exists.

## Examples

```shell
dragonfly> SET key1 "Hello"
OK
dragonfly> COPY key1 key2
(integer) 1
dragonfly> GET key2
"Hello"
```
