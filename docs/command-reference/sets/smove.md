---
description:  Learn how to use Redis SMOVE command to shift a member from a source set to a target set.
---

import PageTitle from '@site/src/components/PageTitle';

# SMOVE

<PageTitle title="Redis SMOVE Command (Documentation) | Dragonfly" />

## Syntax

    SMOVE source destination member

**Time complexity:** O(1)

**ACL categories:** @write, @set, @fast

Move `member` from the set at `source` to the set at `destination`.
This operation is atomic.
In every given moment the element will appear to be a member of `source` **or**
`destination` for other clients.

If the source set does not exist or does not contain the specified element, no
operation is performed and `0` is returned.
Otherwise, the element is removed from the source set and added to the
destination set.
When the specified element already exists in the destination set, it is only
removed from the source set.

An error is returned if `source` or `destination` does not hold a set value.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers), specifically:

* `1` if the element is moved.
* `0` if the element is not a member of `source` and no operation was performed.

## Examples

```shell
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "two"
(integer) 1
dragonfly> SADD myotherset "three"
(integer) 1
dragonfly> SMOVE myset myotherset "two"
(integer) 1
dragonfly> SMEMBERS myset
1) "one"
dragonfly> SMEMBERS myotherset
1) "two"
2) "three"
```
