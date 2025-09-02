---
description: "Make use of Redis EXPIRETIME that returns absolute Unix expiry of a key in seconds."
---

import PageTitle from '@site/src/components/PageTitle';

# EXPIRETIME

<PageTitle title="Redis EXPIRETIME Command (Documentation) | Dragonfly" />

## Syntax

    EXPIRETIME key

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

Returns the absolute Unix timestamp (since January 1, 1970) in seconds at which the given key will expire.

See also the [`PEXPIRETIME`](./pexpiretime.md) command which returns the same information with milliseconds resolution.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers), specifically:

- The expiration Unix timestamp, in seconds.
- `-1` if the key exists but has no expiration time.
- `-2` if the key does not exist.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> EXPIRETIME mykey
(integer) -1
dragonfly> EXPIRETIME missing
(integer) -2
dragonfly> EXPIRE mykey 100
(integer) 1
dragonfly> EXPIRETIME mykey
(integer) 1755753267
```
