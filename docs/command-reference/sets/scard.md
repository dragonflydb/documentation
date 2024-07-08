---
description: Learn how to use Redis SCARD command to get the count of members in a set.
---

import PageTitle from '@site/src/components/PageTitle';

# SCARD

<PageTitle title="Redis SCARD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCARD` command in Redis is used to get the number of members in a set. This is particularly useful for determining the size of a set quickly and efficiently. Typical scenarios for using `SCARD` include checking the count of unique elements, verifying the presence of entries before performing operations, or monitoring the growth of collections over time.

## Syntax

```plaintext
SCARD key
```

## Parameter Explanations

- **key**: The name of the set whose cardinality (number of members) you want to retrieve.

## Return Values

- If the set exists, `SCARD` returns the total number of elements (integer) in the set.
- If the set does not exist, `SCARD` returns `0`.

Example outputs:

- For a non-empty set: `(integer) 4`
- For an empty or non-existent set: `(integer) 0`

## Code Examples

```cli
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "two"
(integer) 1
dragonfly> SADD myset "three"
(integer) 1
dragonfly> SADD myset "four"
(integer) 1
dragonfly> SCARD myset
(integer) 4
dragonfly> DEL myset
(integer) 1
dragonfly> SCARD myset
(integer) 0
```

## Best Practices

- Regularly use `SCARD` to monitor the size of sets, especially when working with dynamically changing data, to avoid unexpected performance issues.
- Utilize `SCARD` before performing operations that rely on a minimum or maximum number of set members to ensure the expected preconditions are met.

## Common Mistakes

- Using `SCARD` on non-set data types will result in an error. Always make sure the key refers to a set.

  ```cli
  dragonfly> SET not_a_set "value"
  OK
  dragonfly> SCARD not_a_set
  (error) WRONGTYPE Operation against a key holding the wrong kind of value
  ```

## FAQs

### What happens if I use `SCARD` on a non-existent key?

If `SCARD` is used on a non-existent key, it simply returns `0`, as there are no members in the set.

### Is `SCARD` an O(1) operation?

Yes, `SCARD` operates in constant time O(1), making it efficient regardless of the size of the set.
