---
description: Get the expiration Unix timestamp for a key
---

# EXPIRETIME

## Syntax

    EXPIRETIME key

**Time complexity:** O(1)

Returns the absolute Unix timestamp (since January 1, 1970) in seconds at which the given key will expire.

See also the `PEXPIRETIME` command which returns the same information with milliseconds resolution.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): Expiration Unix timestamp in seconds, or a negative value in order to signal an error (see the description below).

* The command returns `-1` if the key exists but has no associated expiration time.
* The command returns `-2` if the key does not exist.

## Examples

```cli
SET mykey "Hello"
EXPIREAT mykey 33177117420
EXPIRETIME mykey
```
