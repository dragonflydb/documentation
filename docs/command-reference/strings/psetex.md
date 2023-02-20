---
description: Set the value and expiration in milliseconds of a key
---

# PSETEX

## Syntax

    PSETEX key milliseconds value

**Time complexity:** O(1)

`PSETEX` works exactly like `SETEX` with the sole difference that the expire
time is specified in milliseconds instead of seconds.

## Examples

```shell
dragonfly> PSETEX mykey 1000 "Hello"
"OK"
dragonfly> PTTL mykey
(integer) 1000
dragonfly> GET mykey
"Hello"
```
