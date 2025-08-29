---
description:  Learn how to get random members of a set with the Dragonfly SRANDMEMBER command.
---

import PageTitle from '@site/src/components/PageTitle';

# SRANDMEMBER

<PageTitle title="Dragonfly SRANDMEMBER Command (Documentation) | Dragonfly" />

## Syntax

    SRANDMEMBER key [count]

**Time complexity:** Without the count argument O(1), otherwise O(N) where N is the absolute value of the passed count.

**ACL categories:** @read, @set, @fast

When called with just the key argument, return a random element from the set value stored at key.

If the provided count argument is positive, return an array of distinct elements. The array's length is either count or the set's cardinality (SCARD), whichever is lower.

If called with a negative count, the behavior changes and the command is allowed to return the same element multiple times. In this case, the number of returned elements is the absolute value of the specified count.

## Return

When called without the `count` argument:

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): the random member, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): the random members, or an empty array when `key` does not exist.

## Examples

```shell
dragonfly> SADD myset one two three
(integer) 3
dragonfly> SRANDMEMBER myset
"three"
dragonfly> SRANDMEMBER myset 2
1) "one"
2) "three"
dragonfly> SRANDMEMBER myset -5
1) "two"
2) "one"
3) "one"
4) "one"
5) "two"
```
## Distribution of returned elements

Note that this command is not suitable when you need a guaranteed uniform distribution of the returned elements. 
