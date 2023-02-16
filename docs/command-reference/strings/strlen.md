---
description: Get the length of the value stored in a key
---

# STRLEN

## Syntax

    STRLEN key

**Time complexity:** O(1)

Returns the length of the string value stored at `key`.
An error is returned when `key` holds a non-string value.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the length of the string at `key`, or `0` when `key` does not
exist.

## Examples

```cli
SET mykey "Hello world"
STRLEN mykey
STRLEN nonexisting
```