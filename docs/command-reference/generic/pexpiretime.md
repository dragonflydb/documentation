---
description: "PEXPIRETIME returns absolute Unix expiry of a key in milliseconds."
---

import PageTitle from '@site/src/components/PageTitle';

# PEXPIRETIME

<PageTitle title="Redis PEXPIRETIME Command (Documentation) | Dragonfly" />

## Syntax

    PEXPIRETIME key

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

This command works exactly like [`EXPIRETIME`](./expiretime.md),
but the absolute Unix expiration timestamp of the key is returned in milliseconds instead of seconds.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers), specifically:

- The expiration Unix timestamp, in milliseconds
- `-1` if the key exists but has no expiration time.
- `-2` if the key does not exist.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> PEXPIRETIME mykey
(integer) -1
dragonfly> PEXPIRETIME missing
(integer) -2
dragonfly> EXPIRE mykey 100
(integer) 1
dragonfly> PEXPIRETIME mykey
(integer) 1755753267438
```
