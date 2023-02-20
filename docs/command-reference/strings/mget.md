---
description: Get the values of all the given keys
---

# MGET

## Syntax

    MGET key [key ...]

**Time complexity:** O(N) where N is the number of keys to retrieve.

Returns the values of all specified keys.
For every key that does not hold a string value or does not exist, the special
value `nil` is returned.
Because of this, the operation never fails.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of values at the specified keys.

## Examples

```shell
dragonfly> SET key1 "Hello"
"OK"
dragonfly> SET key2 "World"
"OK"
dragonfly> MGET key1 key2 nonexisting
1) "Hello"
2) "World"
3) (nil)
```
