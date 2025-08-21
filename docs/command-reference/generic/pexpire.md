---
description: "Understand the use of Redis PEXPIRE command to set key expiry in milliseconds."
---

import PageTitle from '@site/src/components/PageTitle';

# PEXPIRE

<PageTitle title="Redis PEXPIRE Command (Documentation) | Dragonfly" />

## Syntax

    PEXPIRE key milliseconds [NX | XX | GT | LT]

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

This command works exactly like `EXPIRE` but the time to live of the key is
specified in milliseconds instead of seconds.
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
dragonfly> PEXPIRE mykey 1500
(integer) 1
dragonfly> TTL mykey
(integer) 2
dragonfly> PTTL mykey
(integer) 1500
dragonfly> PEXPIRE mykey 1 GT
(integer) 0
dragonfly> PTTL mykey
(integer) 1500
dragonfly> PEXPIRE mykey 30000 LT
(integer) 0
dragonfly> PTTL mykey
(integer) 1500
dragonfly> PEXPIRE mykey 111 NX
(integer) 0
dragonfly> PTTL mykey
(integer) 1500
```
