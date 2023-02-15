---
description: Get the expiration Unix timestamp for a key in milliseconds
---

# PEXPIRETIME

## Syntax

    PEXPIRETIME key

**Time complexity:** O(1)

`PEXPIRETIME` has the same semantic as `EXPIRETIME`, but returns the absolute Unix expiration timestamp in milliseconds instead of seconds.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): Expiration Unix timestamp in milliseconds, or a negative value in order to signal an error (see the description below).

* The command returns `-1` if the key exists but has no associated expiration time.
* The command returns `-2` if the key does not exist.

## Examples

```cli
SET mykey "Hello"
PEXPIREAT mykey 33177117420000
PEXPIRETIME mykey
```
