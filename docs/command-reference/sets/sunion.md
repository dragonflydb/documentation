---
description: Learn how to use Redis SUNION command to form a set by combining other sets.
---

import PageTitle from '@site/src/components/PageTitle';

# SUNION

<PageTitle title="Redis SUNION Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SUNION` command in Redis is used to compute the union of multiple sets. This command is particularly useful when you need to combine elements from several sets into one, eliminating duplicates. Typical scenarios include aggregating user permissions from different roles or merging tags from various categories.

## Syntax

```
SUNION key [key ...]
```

## Parameter Explanations

- **key**: The keys of the sets you want to unite. You can specify two or more keys.

## Return Values

The `SUNION` command returns a set of elements that are present in at least one of the specified sets. The result is provided as an array of strings.

### Example Outputs:

- If the sets have overlapping elements:
  ```cli
  dragonfly> SUNION set1 set2
  1) "a"
  2) "b"
  3) "c"
  4) "d"
  ```
- If the sets do not overlap:
  ```cli
  dragonfly> SUNION set1 set3
  1) "a"
  2) "e"
  3) "f"
  ```

## Code Examples

Using the CLI:

```cli
dragonfly> SADD set1 "a" "b" "c"
(integer) 3
dragonfly> SADD set2 "b" "c" "d"
(integer) 3
dragonfly> SADD set3 "e" "f"
(integer) 2
dragonfly> SUNION set1 set2
1) "a"
2) "b"
3) "c"
4) "d"
dragonfly> SUNION set1 set3
1) "a"
2) "c"
3) "b"
4) "e"
5) "f"
dragonfly> SUNION set2 set3
1) "b"
2) "c"
3) "d"
4) "e"
5) "f"
```

## Best Practices

- Ensure the sets exist before performing the `SUNION` operation.
- Consider using the `SUNIONSTORE` command if you need to store the union result for future use, which avoids recomputation.

## Common Mistakes

- Using non-set data types with `SUNION` will result in errors. Always ensure the keys refer to sets.
- Forgetting that `SUNION` does not modify any of the input sets but only returns the union.

## FAQs

### What happens if one or more keys do not exist?

If a key does not exist, `SUNION` treats it as an empty set. The command still returns the union of the existing sets.

### Can I use `SUNION` with just one set?

Yes, `SUNION` with a single set will return all elements of that set.
