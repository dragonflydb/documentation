---
description: "Use Redis PEXPIREAT command sets a key's time-to-live in UNIX time."
---

import PageTitle from '@site/src/components/PageTitle';

# PEXPIREAT

<PageTitle title="Redis PEXPIREAT Command (Documentation) | Dragonfly" />

## Syntax

    PEXPIREAT key unix-time-milliseconds [NX | XX | GT | LT]

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

`PEXPIREAT` has the same effect and semantic as `EXPIREAT`, but the Unix time at
which the key will expire is specified in milliseconds instead of seconds.
If `NX` option is specified, the field data will not be overwritten.
If `XX` option is specified, expiry will only be set if there is an existing expiry.
If `GT` option is specified, expiry will only be set if new value is greater than current value.
If `LT` option is specified, expiry will only be set if the new value is less than current value.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

- `1` if the timeout was set.
- `0` if the timeout was not set. e.g. key doesn't exist, or operation skipped due to the provided arguments.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> PEXPIREAT mykey 1555555555005
(integer) 1
dragonfly> TTL mykey
(integer) -2
dragonfly> PTTL mykey
(integer) -2
```
