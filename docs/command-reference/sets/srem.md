---
description: Learn how to use Redis SREM command to remove specified members from a set.
---

import PageTitle from '@site/src/components/PageTitle';

# SREM

<PageTitle title="Redis SREM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SREM` command in Redis is used to remove one or more specified members from a set. It is particularly useful for maintaining dynamic sets, such as removing users from groups or tags from resources.

## Syntax

```plaintext
SREM key member [member ...]
```

## Parameter Explanations

- `key`: The key of the set from which you want to remove members.
- `member`: One or more members that you wish to remove from the set.

## Return Values

`SREM` returns an integer which represents the number of members that were removed from the set. If the specified members are not part of the set, it returns 0.

Example outputs:

- `(integer) 1`: If one member was successfully removed.
- `(integer) 0`: If none of the specified members were found in the set.

## Code Examples

```cli
dragonfly> SADD myset "one" "two" "three"
(integer) 3
dragonfly> SREM myset "two"
(integer) 1
dragonfly> SREM myset "four"
(integer) 0
dragonfly> SMEMBERS myset
1) "one"
2) "three"
```

## Best Practices

- Ensure the key exists and is of type set before using `SREM`.
- Use `SISMEMBER` to check if a member exists before attempting to remove it, especially in performance-sensitive applications.

## Common Mistakes

- Using `SREM` on keys that are not sets will result in an error.
- Misunderstanding the return value; `0` means no members were removed, not necessarily an error.

## FAQs

### What happens if I try to remove a member that doesn't exist in the set?

If a member does not exist in the set, `SREM` simply returns `0` indicating no members were removed.

### Can I use `SREM` with multiple members at once?

Yes, you can specify multiple members in the `SREM` command to remove them in a single operation.
