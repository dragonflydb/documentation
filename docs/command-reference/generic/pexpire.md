---
description: Set a key's time to live in milliseconds
---

# PEXPIRE

## Syntax

    PEXPIRE key milliseconds [NX | XX | GT | LT]

**Time complexity:** O(1)

This command works exactly like `EXPIRE` but the time to live of the key is
specified in milliseconds instead of seconds.

## Options

The `PEXPIRE` command supports a set of options since Redis 7.0:

* `NX` -- Set expiry only when the key has no expiry
* `XX` -- Set expiry only when the key has an existing expiry
* `GT` -- Set expiry only when the new expiry is greater than current one
* `LT` -- Set expiry only when the new expiry is less than current one

A non-volatile key is treated as an infinite TTL for the purpose of `GT` and `LT`.
The `GT`, `LT` and `NX` options are mutually exclusive.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if the timeout was set.
* `0` if the timeout was not set. e.g. key doesn't exist, or operation skipped due to the provided arguments.

## Examples

```shell
dragonfly> SET mykey "Hello"
"OK"
dragonfly> PEXPIRE mykey 1500
(integer) 1
dragonfly> TTL mykey
(integer) 2
dragonfly> PTTL mykey
(integer) 1500
dragonfly> PEXPIRE mykey 1000 XX
(integer) 1
dragonfly> TTL mykey
(integer) 1
dragonfly> PEXPIRE mykey 1000 NX
(integer) 0
dragonfly> TTL mykey
(integer) 1
```
