---
description: Get the time to live for a key in milliseconds
---

# PTTL

## Syntax

    PTTL key

**Time complexity:** O(1)

Like `TTL` this command returns the remaining time to live of a key that has an
expire set, with the sole difference that `TTL` returns the amount of remaining
time in seconds while `PTTL` returns it in milliseconds.

In Redis 2.6 or older the command returns `-1` if the key does not exist or if the key exist but has no associated expire.

Starting with Redis 2.8 the return value in case of error changed:

* The command returns `-2` if the key does not exist.
* The command returns `-1` if the key exists but has no associated expire.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): TTL in milliseconds, or a negative value in order to signal an error (see the description above).

## Examples

```shell
dragonfly> SET mykey "Hello"
"OK"
dragonfly> EXPIRE mykey 1
(integer) 1
dragonfly> PTTL mykey
(integer) 1000
```
