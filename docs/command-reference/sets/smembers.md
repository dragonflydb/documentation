---
description: Learn how to get all members of a set with the Redis SMEMBERS command.
---

import PageTitle from '@site/src/components/PageTitle';

# SMEMBERS

<PageTitle title="Redis SMEMBERS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`SMEMBERS` is a Redis command used to return all the members of a set. This command is particularly useful when you need to retrieve the entire set of unique elements stored under a specific key. Typical use cases include getting all tags assigned to a blog post, listing all users in a chat room, or fetching all permissions assigned to a user.

## Syntax

```cli
SMEMBERS key
```

## Parameter Explanations

- **key**: The name of the set from which you want to retrieve all the members. This parameter is mandatory.

## Return Values

`SMEMBERS` returns an array of the members in the set. If the specified key does not exist, it returns an empty array.

Example outputs:

- If the set contains members: `["member1", "member2", "member3"]`
- If the set is empty or does not exist: `[]`

## Code Examples

```cli
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "two"
(integer) 1
dragonfly> SADD myset "three"
(integer) 1
dragonfly> SMEMBERS myset
1) "one"
2) "two"
3) "three"

dragonfly> SADD emptyset
(integer) 0
dragonfly> SMEMBERS emptyset
(empty array)
```

## Best Practices

- When using `SMEMBERS`, be mindful that if the set has a large number of elements, retrieving all of them at once might cause performance issues. Consider using `SSCAN` for large sets to iterate over the elements incrementally.

## Common Mistakes

- Using `SMEMBERS` with a non-set key type will result in a type error. Ensure the key you're querying actually stores a set.
- Not handling the case where the set is empty or does not exist can lead to unexpected empty results.

## FAQs

### What happens if the key does not exist?

If the specified key does not exist, `SMEMBERS` returns an empty array.

### Can I use SMEMBERS on keys with different data types?

No, `SMEMBERS` should only be used with keys storing sets. Using it with other data types will result in an error.

### How to handle large sets with SMEMBERS?

For large sets, consider using the `SSCAN` command to iterate over the elements in smaller chunks rather than retrieving all elements at once.
