---
description: Get the score associated with the given members in a sorted set
---

# ZMSCORE

## Syntax

    ZMSCORE key member [member ...]

**Time complexity:** O(N) where N is the number of members being requested.

Returns the scores associated with the specified `members` in the sorted set stored at `key`.

For every `member` that does not exist in the sorted set, a `nil` value is returned.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of scores or `nil` associated with the specified `member` values (a double precision floating point number),
represented as strings.

## Examples

```cli
ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZMSCORE myzset "one" "two" "nofield"
```
