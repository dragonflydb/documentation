---
description: Merge N different HyperLogLogs into a single one.
---

# PFMERGE

## Syntax

    PFMERGE destkey [sourcekey [sourcekey ...]]

**Time complexity:** O(N) to merge N HyperLogLogs, but with high constant times.

Merge multiple HyperLogLog values into a unique value that will approximate
the cardinality of the union of the observed Sets of the source HyperLogLog
structures.

The computed merged HyperLogLog is set to the destination variable, which is
created if does not exist (defaulting to an empty HyperLogLog).

If the destination variable exists, it is treated as one of the source sets 
and its cardinality will be included in the cardinality of the computed
HyperLogLog.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): The command just returns `OK`.

## Examples

```cli
PFADD hll1 foo bar zap a
PFADD hll2 a b c foo
PFMERGE hll3 hll1 hll2
PFCOUNT hll3
```
