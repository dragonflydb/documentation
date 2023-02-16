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

```cli
PSETEX mykey 1000 "Hello"
PTTL mykey
GET mykey
```
