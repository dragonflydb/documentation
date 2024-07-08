---
description: Learn how to use Redis SDIFFSTORE command to extract the difference of sets and store it.
---

import PageTitle from '@site/src/components/PageTitle';

# SDIFFSTORE

<PageTitle title="Redis SDIFFSTORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`SDIFFSTORE` is a Redis command used to compute the difference between multiple sets and store the result in a new set. It subtracts all the subsequent sets from the first set and saves the resulting set into the destination key. This is useful for operations where you need to persist the difference between sets, such as filtering out elements that are common in several sets.

## Syntax

```plaintext
SDIFFSTORE destination key [key ...]
```

## Parameter Explanations

- **destination**: The key where the result of the difference operation will be stored.
- **key**: The keys of the sets involved in the difference operation. The first key is the base set, and each of the next keys' elements will be subtracted from it.

## Return Values

`SDIFFSTORE` returns the number of elements in the resulting set stored at the destination key.

Example output:

```plaintext
(integer) 3
```

## Code Examples

```cli
dragonfly> SADD set1 "a" "b" "c"
(integer) 3
dragonfly> SADD set2 "c" "d" "e"
(integer) 3
dragonfly> SADD set3 "a" "f"
(integer) 2
dragonfly> SDIFFSTORE resultSet set1 set2 set3
(integer) 1
dragonfly> SMEMBERS resultSet
1) "b"
```

## Best Practices

- Ensure that the sets involved in the `SDIFFSTORE` operation exist and contain the expected elements to avoid unexpected results.
- Use `SDIFF` to preview the result before using `SDIFFSTORE`, ensuring accuracy before storing the data.

## Common Mistakes

- Using non-set keys with `SDIFFSTORE` can result in errors or unexpected behavior. Always confirm that keys are associated with valid sets.
- Overwriting existing keys unintentionally if the destination key already exists. Always check if this key needs to be overwritten or renamed.

## FAQs

### What happens if the destination key already exists?

The `SDIFFSTORE` command will overwrite the existing destination key with the computed set difference.

### Can I use `SDIFFSTORE` with only one set?

While technically possible, using `SDIFFSTORE` with one set is redundant and will simply copy the set to the destination key.
