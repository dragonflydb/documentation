---
description:  Learn how to use Redis SMISMEMBER command to verify the membership of multiple keys in a set.
---

import PageTitle from '@site/src/components/PageTitle';

# SMISMEMBER

<PageTitle title="Redis SMISMEMBER Command (Documentation) | Dragonfly" />

## Syntax

    SMISMEMBER key member [member ...]

**Time complexity:** O(N) where N is the number of elements being checked for membership

**ACL categories:** @read, @set, @fast

Returns whether each `member` is a member of the set stored at `key`.

For every `member`, `1` is returned if the value is a member of the set, or `0` if the element is not a member of the set or if `key` does not exist.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): list representing the membership of the given elements, in the same
order as they are requested.

## Examples

```shell
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "one"
(integer) 0
dragonfly> SMISMEMBER myset "one" "notamember"
1) (integer) 1
2) (integer) 0
```
