---
description: Determine if a given value is a member of a set
---

# SISMEMBER

## Syntax

    SISMEMBER key member

**Time complexity:** O(1)

**ACL categories:** @read, @set, @fast

Returns if `member` is a member of the set stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

* `1` if the element is a member of the set.
* `0` if the element is not a member of the set, or if `key` does not exist.

## Examples

```shell
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SISMEMBER myset "one"
(integer) 1
dragonfly> SISMEMBER myset "two"
(integer) 0
```
