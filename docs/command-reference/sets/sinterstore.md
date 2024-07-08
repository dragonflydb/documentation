---
description: Learn how to use Redis SINTERSTORE command to find the intersection of sets and store the result.
---

import PageTitle from '@site/src/components/PageTitle';

# SINTERSTORE

<PageTitle title="Redis SINTERSTORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`SINTERSTORE` is a Redis command used to compute the intersection of multiple sets and store the resulting set in a new key. This is particularly useful when you need to find common elements across several datasets and want to store the result for future use, saving computational overhead.

## Syntax

```plaintext
SINTERSTORE destination key [key ...]
```

## Parameter Explanations

- **destination**: The key where the result of the set intersection will be stored.
- **key [key ...]**: One or more keys of the sets to intersect.

## Return Values

`SINTERSTORE` returns the number of elements in the resulting set.

### Example Outputs:

- When there are common elements:
  ```plaintext
  (integer) 2
  ```
- When there are no common elements:
  ```plaintext
  (integer) 0
  ```

## Code Examples

```cli
dragonfly> SADD set1 "a" "b" "c"
(integer) 3
dragonfly> SADD set2 "b" "c" "d"
(integer) 3
dragonfly> SADD set3 "c" "e" "f"
(integer) 3
dragonfly> SINTERSTORE result set1 set2 set3
(integer) 1
dragonfly> SMEMBERS result
1) "c"
```

## Best Practices

- Ensure the keys being intersected exist and are of type set to avoid unexpected behavior.
- Use `EXISTS` command to check if the destination key already exists, as `SINTERSTORE` will overwrite any existing key with the same name.

## Common Mistakes

- Using non-set keys with `SINTERSTORE` will result in an error.
- Not handling empty intersections can lead to confusion; always check the result count.

## FAQs

### What happens if one of the keys does not exist?

If one or more keys do not exist, Redis treats them as empty sets, which might affect the intersection result.

### Can `SINTERSTORE` be used with only one set?

Yes, but it is essentially equivalent to copying the set to the destination key.
