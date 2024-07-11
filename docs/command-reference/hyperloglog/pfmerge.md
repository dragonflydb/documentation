---
description: Discover the use of Redis PFMERGE command for merging multiple HyperLogLog data structures.
---
import PageTitle from '@site/src/components/PageTitle';

# PFMERGE

<PageTitle title="Redis PFMERGE Command (Documentation) | Dragonfly" />

## Syntax

    PFMERGE destkey [sourcekey [sourcekey ...]]

**Time complexity:** O(N) to merge N HyperLogLogs, but with high constant times.

**ACL categories:** @write, @hyperloglog, @slow

Merge multiple HyperLogLog values into a unique value that will approximate the cardinality of the
union of the observed Sets of the source HyperLogLog structures.

The computed merged HyperLogLog is set to the destination variable, which is created if does not
exist (defaulting to an empty HyperLogLog).

If the destination variable exists, it is treated as one of the source sets and its cardinality will
be included in the cardinality of the computed HyperLogLog.


## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): The
command just returns OK.

## Examples

```shell
dragonfly> PFADD hll1 foo bar zap a
(integer) 1
dragonfly> PFADD hll2 a b c foo
(integer) 1
dragonfly> PFMERGE hll3 hll1 hll2
OK
dragonfly> PFCOUNT hll3
(integer) 6
```
