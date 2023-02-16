---
description: Returns the membership associated with the given elements for a set
---

# SMISMEMBER

## Syntax

    SMISMEMBER key member [member ...]

**Time complexity:** O(N) where N is the number of elements being checked for membership

Returns whether each `member` is a member of the set stored at `key`.

For every `member`, `1` is returned if the value is a member of the set, or `0` if the element is not a member of the set or if `key` does not exist.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list representing the membership of the given elements, in the same
order as they are requested.

## Examples

```cli
SADD myset "one"
SADD myset "one"
SMISMEMBER myset "one" "notamember"
```
