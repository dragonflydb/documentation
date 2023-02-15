---
description: Determine if a given value is a member of a set
---

# SISMEMBER

## Syntax

    SISMEMBER key member

**Time complexity:** O(1)

Returns if `member` is a member of the set stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if the element is a member of the set.
* `0` if the element is not a member of the set, or if `key` does not exist.

## Examples

```cli
SADD myset "one"
SISMEMBER myset "one"
SISMEMBER myset "two"
```
