---
description: Learn how to use Redis SADD command to add one or more members to a set.
---

import PageTitle from '@site/src/components/PageTitle';

# SADD

<PageTitle title="Redis SADD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SADD` command in Redis is used to add one or more members to a set stored at a key. If the key does not exist, a new set is created before adding the members. This command is useful for maintaining collections of unique items where duplicate entries are automatically ignored.

## Syntax

```
SADD key member [member ...]
```

## Parameter Explanations

- **key**: The name of the set.
- **member**: One or more members to be added to the set. Each must be unique within the set.

## Return Values

The `SADD` command returns an integer representing the number of elements that were added to the set, excluding all elements already present in the set.

### Examples:

1. Adding new members:

   ```
   (integer) 1
   ```

2. Adding existing members:

   ```
   (integer) 0
   ```

3. Adding multiple members where some are new and some are duplicates:
   ```
   (integer) 2
   ```

## Code Examples

```cli
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "two"
(integer) 1
dragonfly> SADD myset "two"
(integer) 0
dragonfly> SADD myset "three" "four"
(integer) 2
dragonfly> SMEMBERS myset
1) "one"
2) "two"
3) "three"
4) "four"
```

## Best Practices

- Always check if a set exists before assuming you know its content. Using `SMEMBERS` can help verify the current state of the set.
- When adding multiple members, group them in a single `SADD` command to minimize round trips to the server.

## Common Mistakes

- Assuming `SADD` can operate on non-set data types. Make sure the key represents a set.
- Forgetting that the return value excludes already existing members, which could lead to misunderstandings about how many new elements were truly added.

## FAQs

### What happens if I try to add an element that already exists in the set?

Redis will simply ignore the duplicate member and it won't be added again. The return value will reflect only the number of new entries added.

### Can I use non-string data types as members in the set?

No, all members of a Redis set must be strings. Attempting to add other data types will result in an error.
