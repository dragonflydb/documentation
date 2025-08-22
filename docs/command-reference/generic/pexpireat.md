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

## Options

- `NX`: Expiry will only be set if the key has no expiry.
- `XX`: Expiry will only be set if the key has an existing expiry.
- `GT`: Expiry will only be set if the new expiry is greater than current one.
- `LT`: Expiry will only be set if the new expiry is less than current one.

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
