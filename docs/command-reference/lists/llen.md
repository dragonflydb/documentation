---
description: Get the length of a list
---

# LLEN

## Syntax

    LLEN key

**Time complexity:** O(1)

Returns the length of the list stored at `key`.
If `key` does not exist, it is interpreted as an empty list and `0` is returned.
An error is returned when the value stored at `key` is not a list.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the length of the list at `key`.

## Examples

```cli
LPUSH mylist "World"
LPUSH mylist "Hello"
LLEN mylist
```
