---
description: Discover the use of Redis PFMERGE command for merging multiple HyperLogLog data structures.
---

import PageTitle from '@site/src/components/PageTitle';

# PFMERGE

<PageTitle title="Redis PFMERGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`PFMERGE` is a Redis command used to merge multiple HyperLogLog data structures into a single HyperLogLog. This is particularly useful when you want to combine the approximations of distinct elements from different sets. Typical use cases include merging user activity logs from multiple shards, aggregating statistics, or combining results from distributed computations.

## Syntax

```plaintext
PFMERGE destkey sourcekey [sourcekey ...]
```

## Parameter Explanations

- **destkey**: The key where the merged HyperLogLog will be stored.
- **sourcekey**: One or more keys of the HyperLogLogs that you want to merge.

## Return Values

The command returns `OK` if the merge operation is successful. If any of the source keys do not contain a valid HyperLogLog, an error is returned.

## Code Examples

```cli
dragonfly> PFADD hll1 "a" "b" "c"
(integer) 1
dragonfly> PFADD hll2 "b" "c" "d"
(integer) 1
dragonfly> PFADD hll3 "d" "e" "f"
(integer) 1
dragonfly> PFMERGE hllmerged hll1 hll2 hll3
OK
dragonfly> PFCOUNT hllmerged
(integer) 6
```

## Best Practices

When using `PFMERGE`, ensure that all the sourcekeys contain valid HyperLogLog structures. This prevents errors and ensures accurate merging of the datasets.

## Common Mistakes

- **Invalid HyperLogLog Keys**: Attempting to merge keys that do not contain HyperLogLog structures will result in an error.
- **Overwriting Existing Data**: Be cautious when specifying `destkey`. If it already exists, its data will be overwritten with the merged result.

## FAQs

### Can I merge HyperLogLogs with non-HyperLogLog keys?

No, all source keys must be HyperLogLogs. Attempting to merge a HyperLogLog with a non-HyperLogLog key will result in an error.

### What happens if `destkey` already exists?

If `destkey` already exists, the existing data will be overwritten by the merged result of the specified sourcekeys.
