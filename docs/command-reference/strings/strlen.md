---
description: Get the length of the value stored in a key
---

# STRLEN

## Syntax

    STRLEN key

**Time complexity:** O(1)

**ACL categories:** @read, @string, @fast

Returns the length of the string value stored at `key`.
An error is returned when `key` holds a non-string value.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the length of the string at `key`, or `0` when `key` does not
exist.

## Examples

```shell
dragonfly> SET mykey "Hello world"
"OK"
dragonfly> STRLEN mykey
(integer) 11
dragonfly> STRLEN nonexisting
(integer) 0
```
