---
description:  Learn how to use Redis SADDEX command adding in a value only if it does not exist.
---

import PageTitle from '@site/src/components/PageTitle';

# SADDEX

<PageTitle title="Redis SADDEX Command (Documentation) | Dragonfly" />

## Syntax

    SADDEX key [KEEPTTL] seconds member [member ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @set, @fast

**Warning:** Experimental! Dragonfly-specific.

Similar to [`SADD`](sadd.md) but adds one or more members that expire after specified number of seconds.

If the `KEEPTTL` option is specified, any existing members will preserve their TTL, and the supplied value 
will only be applied to new members.

An error is returned when the value stored at `key` is not a set. 

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of elements that were added to the set, not including all the elements already present in the set.

## Examples

```shell
dragonfly> SADDEX myset 10 "Hello"
(integer) 1
dragonfly> SADDEX myset 20 World Dragonfly
(integer) 2
dragonfly> SMEMBERS myset
1) "Hello"
2) "World"
3) "Dragonfly"
```
