---
description: Set the expiration for a key as a UNIX timestamp
---

# EXPIREAT

## Syntax

    EXPIREAT key unix-time-seconds

**Time complexity:** O(1)

`EXPIREAT` has the same effect and semantic as `EXPIRE`, but instead of
specifying the number of seconds representing the TTL (time to live), it takes
an absolute [Unix timestamp][hewowu] (seconds since January 1, 1970). A
timestamp in the past will delete the key immediately.

[hewowu]: http://en.wikipedia.org/wiki/Unix_time

Please for the specific semantics of the command refer to the documentation of
`EXPIRE`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if the timeout was set.
* `0` if the timeout was not set. e.g. key doesn't exist, or operation skipped due to the provided arguments.

## Examples

```shell
dragonfly> SET mykey "Hello"
"OK"
dragonfly> EXISTS mykey
(integer) 1
dragonfly> EXPIREAT mykey 1293840000
(integer) 1
dragonfly> EXISTS mykey
(integer) 0
```
