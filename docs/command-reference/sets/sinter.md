---
description: Learn how to use Redis SINTER command to get the intersection of multiple sets.
---

import PageTitle from '@site/src/components/PageTitle';

# SINTER

<PageTitle title="Redis SINTER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SINTER` command in Redis is used to find the intersection of multiple sets. This means it returns members that are present in all the given sets. It's typically used in scenarios where you need to identify common elements shared among different groupings.

## Syntax

```plaintext
SINTER key [key ...]
```

## Parameter Explanations

- `key`: The name of the set. You can specify two or more keys, and `SINTER` will return members that exist in all specified sets.

## Return Values

`SINTER` returns an array of elements that are common to all provided sets. If no element exists in all sets, it returns an empty array.

Example outputs:

- If there is an intersection: `["member1", "member2"]`
- If there is no intersection: `[]`

## Code Examples

```cli
dragonfly> SADD set1 "a" "b" "c"
(integer) 3
dragonfly> SADD set2 "b" "c" "d"
(integer) 3
dragonfly> SADD set3 "c" "e" "f"
(integer) 3
dragonfly> SINTER set1 set2 set3
1) "c"
```

## Best Practices

- Ensure that the sets are not empty to avoid returning an empty intersection.
- Use `SINTERSTORE` if you want to store the result of the intersection directly into a new set.

## Common Mistakes

- Forgetting that `SINTER` requires at least two sets to perform an intersection, leading to incorrect usage or unexpected results.

## FAQs

### What happens if one of the sets does not exist?

If one or more of the specified sets do not exist, `SINTER` treats them as empty sets, which results in an empty intersection.

### Can `SINTER` be used with more than two sets?

Yes, `SINTER` can be used with any number of sets. It will return the intersection of all provided sets.
