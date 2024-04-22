---
description: "Learn Redis RENAME command which renames a key."
---

import PageTitle from '@site/src/components/PageTitle';

# RENAME

<PageTitle title="Redis RENAME Command (Documentation) | Dragonfly" />

## Syntax

    RENAME key newkey

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @slow

Renames `key` to `newkey`.
It returns an error when `key` does not exist.
If `newkey` already exists it is overwritten, when this happens `RENAME` executes an implicit `DEL` operation, so if the deleted key contains a very big value it may cause high latency even if `RENAME` itself is usually a constant-time operation.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings)

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> RENAME mykey myotherkey
OK
dragonfly> GET myotherkey
"Hello"
```
