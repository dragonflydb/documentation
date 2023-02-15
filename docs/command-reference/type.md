---
description: Determine the type stored at key
---

# TYPE

## Syntax

    TYPE key

**Time complexity:** O(1)

Returns the string representation of the type of the value stored at `key`.
The different types that can be returned are: `string`, `list`, `set`, `zset`,
`hash` and `stream`.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): type of `key`, or `none` when `key` does not exist.

## Examples

```cli
SET key1 "value"
LPUSH key2 "value"
SADD key3 "value"
TYPE key1
TYPE key2
TYPE key3
```
