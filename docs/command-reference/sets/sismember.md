---
description: Learn how to use Redis SISMEMBER command, to check if a given value is present in a set.
---

import PageTitle from '@site/src/components/PageTitle';

# SISMEMBER

<PageTitle title="Redis SISMEMBER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SISMEMBER` command in Redis is used to determine if a given value is a member of a set. This command is particularly useful when you need to verify the existence of an element within a set, such as checking if a user ID exists in a set of banned users or verifying if a specific item belongs to a collection.

## Syntax

```plaintext
SISMEMBER key member
```

## Parameter Explanations

- **key**: The name of the set where the search will take place. It should be a valid string representing the set's identifier.
- **member**: The value you want to check for membership in the specified set.

## Return Values

The `SISMEMBER` command returns an integer:

- `1`: The member exists in the set.
- `0`: The member does not exist in the set.

Example:

```cli
dragonfly> SISMEMBER myset "value"
(integer) 1
dragonfly> SISMEMBER myset "nonexistent"
(integer) 0
```

## Code Examples

Add elements to a set and check their membership:

```cli
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "two"
(integer) 1
dragonfly> SISMEMBER myset "one"
(integer) 1
dragonfly> SISMEMBER myset "three"
(integer) 0
```

## Best Practices

- Use `SISMEMBER` to quickly check for the presence of an element in a set without iterating through the set manually.
- Combine `SISMEMBER` with conditional logic in your application to handle cases when the member exists or doesn't exist in the set.

## Common Mistakes

- Using `SISMEMBER` on a key that is not of set type will result in an error. Ensure that the key references a set.
- Not handling the return values properly might lead to incorrect application logic. Always check if the returned integer is `1` or `0`.

### FAQs

### How does SISMEMBER perform with large sets?

`SISMEMBER` is optimized for performance even with large sets due to Redis's efficient data structures and hashing mechanisms.

### Can I use SISMEMBER with other Redis data types?

No, `SISMEMBER` is specifically designed for sets. Using it with strings, lists, or hashes will result in an error.
