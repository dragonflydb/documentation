---
description: Learn how to use Redis SDIFF command to get the difference from the first set against all the other sets.
---

import PageTitle from '@site/src/components/PageTitle';

# SDIFF

<PageTitle title="Redis SDIFF Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SDIFF` command in Redis is used to return the members of the set resulting from the difference between the first set and all successive sets. This can be useful for scenarios where you need to find unique elements in one set that are not present in another, such as finding items exclusive to a particular user, or identifying differences between datasets.

## Syntax

```
SDIFF key [key ...]
```

## Parameter Explanations

- **key**: The keys representing the sets you want to compare. The first key is the base set from which the differences will be calculated against the subsequent sets.

## Return Values

The command returns an array of members that are present in the first set but not in any of the subsequent sets.

### Example Outputs:

1. When there are unique members:

   ```
   dragonfly> SDIFF set1 set2
   1) "a"
   2) "b"
   ```

2. When there are no unique members:
   ```
   dragonfly> SDIFF set1 set2
   (empty array)
   ```

## Code Examples

```cli
dragonfly> SADD set1 "a" "b" "c"
(integer) 3
dragonfly> SADD set2 "c" "d" "e"
(integer) 3
dragonfly> SDIFF set1 set2
1) "a"
2) "b"
dragonfly> SADD set3 "a"
(integer) 1
dragonfly> SDIFF set1 set3
1) "b"
2) "c"
```

## Best Practices

- Ensure the sets involved are appropriate for the difference operation to avoid unnecessary computational overhead.
- Consider using `SDIFFSTORE` if you need to store the result of the difference operation for further use.

## Common Mistakes

- Using non-set data types with `SDIFF` can lead to errors or unexpected results.
- Forgetting that the operation is performed in the order provided; the first set is treated as the base set.

## FAQs

### What happens if one of the keys does not exist?

If a key does not exist, it is considered an empty set in the context of the `SDIFF` operation.

### Can I use `SDIFF` with more than two sets?

Yes, you can provide multiple sets. Redis will compute the difference sequentially from the first set to each of the subsequent sets.
