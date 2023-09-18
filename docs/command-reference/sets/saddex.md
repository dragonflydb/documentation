---
description: Add one or more expiring members to a set
---

# SADDEX

## Syntax

    SADDEX key seconds member [member ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @set, @fast

**Warning:** Experimental! Dragonfly specific.

Similar to SADD but adds one or more members that expire after specified number of seconds.
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
