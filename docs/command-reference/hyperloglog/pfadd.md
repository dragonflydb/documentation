---
description: Learn how to use Redis PFADD command for adding elements to HyperLogLog data structure.
---
import PageTitle from '@site/src/components/PageTitle';

# PFADD

<PageTitle title="Redis PFADD Command (Documentation) | Dragonfly" />

## Syntax

    PFADD key [element [element ...]]

**Time complexity:** O(1) for each element added.

**ACL categories:** @write, @hyperloglog, @fast

Adds all the element arguments to the HyperLogLog data structure stored at the variable name
specified as first argument.

As a side effect of this command the HyperLogLog internals may be updated to reflect a different
estimation of the number of unique items added so far (the cardinality of the set).

If the approximated cardinality estimated by the HyperLogLog changed after executing the command,
`PFADD` returns 1, otherwise 0 is returned. The command automatically creates an empty HyperLogLog
structure (that is, a string of a specified length and with a given encoding) if the specified key
does not exist.

It is valid to call the command without elements with only the key name. This will result in no
operation being performed if the key already exists, or in the creation of the data structure if
the key does not exist (in the latter case 1 is returned).

For an introduction to the HyperLogLog data structure, check the `PFCOUNT` command page.


## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers), specifically:
*  1 if at least 1 HyperLogLog internal register was altered. 0 otherwise.

## Examples

```shell
dragonfly> PFADD hll a b c d e f g
(integer) 1
dragonfly> PFCOUNT hll
(integer) 7
```
