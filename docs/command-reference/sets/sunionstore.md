---
description: Learn how to use Redis SUNIONSTORE command to combine multiple sets and store the result in a new set.
---

import PageTitle from '@site/src/components/PageTitle';

# SUNIONSTORE

<PageTitle title="Redis SUNIONSTORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SUNIONSTORE` command in Redis is used to perform a union of multiple sets and store the result in a new set. This is particularly useful when you need to combine different groups of elements into a single collection without duplicates and reuse it later.

## Syntax

```plaintext
SUNIONSTORE destination key [key ...]
```

## Parameter Explanations

- `destination`: The key where the resulting set will be stored.
- `key`: One or more keys representing the sets to be unioned.

## Return Values

- (Integer): The number of elements in the resulting set.

Example:

```plaintext
(integer) 3
```

## Code Examples

```cli
dragonfly> SADD set1 "a" "b" "c"
(integer) 3
dragonfly> SADD set2 "c" "d" "e"
(integer) 3
dragonfly> SUNIONSTORE resultset set1 set2
(integer) 5
dragonfly> SMEMBERS resultset
1) "a"
2) "b"
3) "c"
4) "d"
5) "e"
```

## Best Practices

- Ensure that the `destination` key is different from the input keys to avoid overwriting data unintentionally.

## Common Mistakes

- Trying to use `SUNIONSTORE` with non-set keys will result in an error. Make sure all specified keys point to sets.

---

## FAQs

### What happens if one or more of the input keys do not exist?

If any of the input keys do not exist, they are treated as empty sets and the union operation proceeds with the existing sets.

### Can I use `SUNIONSTORE` with only one set?

Yes, but it's redundant. Using `SUNIONSTORE` with a single set simply copies the set to the destination.
