---
description: Set the expiration for a key as a UNIX timestamp specified in milliseconds
---

# PEXPIREAT

## Syntax

    PEXPIREAT key unix-time-milliseconds

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

`PEXPIREAT` has the same effect and semantic as `EXPIREAT`, but the Unix time at
which the key will expire is specified in milliseconds instead of seconds.


## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if the timeout was set.
* `0` if the timeout was not set. e.g. key doesn't exist, or operation skipped due to the provided arguments.

## Examples

```shell
dragonfly> SET mykey "Hello"
"OK"
dragonfly> PEXPIREAT mykey 1555555555005
(integer) 1
dragonfly> TTL mykey
(integer) -2
dragonfly> PTTL mykey
(integer) -2
```
