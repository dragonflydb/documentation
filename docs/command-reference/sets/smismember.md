---
description: Learn how to use Redis SMISMEMBER command to verify the membership of multiple keys in a set.
---

import PageTitle from '@site/src/components/PageTitle';

# SMISMEMBER

<PageTitle title="Redis SMISMEMBER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`SMISMEMBER` is a Redis command used to check the existence of multiple members in a set. It is particularly useful when you need to verify the presence of several items at once without issuing multiple `SISMEMBER` commands. Typical scenarios include validating user IDs in an active session set or checking if certain tags exist within a predefined tag set.

## Syntax

```cli
SMISMEMBER key member [member ...]
```

## Parameter Explanations

- `key`: The name of the set where the members will be checked.
- `member [member ...]`: One or more members whose existence you want to verify in the set.

## Return Values

The command returns an array of integers. Each integer corresponds to the presence of the respective member:

- `1`: The member exists in the set.
- `0`: The member does not exist in the set.

Example:
For a set with `{"one", "two"}`:

- `dragonfly> SMISMEMBER myset one two three`
  - `1) 1`
  - `2) 1`
  - `3) 0`

## Code Examples

```cli
dragonfly> SADD myset "one" "two"
(integer) 2
dragonfly> SMISMEMBER myset "one" "two" "three"
1) (integer) 1
2) (integer) 1
3) (integer) 0
dragonfly> SMISMEMBER myset "four"
1) (integer) 0
```

## Best Practices

- Use `SMISMEMBER` instead of multiple `SISMEMBER` calls to reduce network round trips and improve performance.

## Common Mistakes

- Forgetting that the command checks for multiple members and mistakenly using it for a single member, which can still work but misses the optimization benefits.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `SMISMEMBER` treats it as an empty set and returns `0` for all queried members.

### Can I use `SMISMEMBER` with non-set data types?

No, `SMISMEMBER` is specific to sets. Using it with other data types will result in an error.
