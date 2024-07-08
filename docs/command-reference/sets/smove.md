---
description: Learn how to use Redis SMOVE command to shift a member from a source set to a target set.
---

import PageTitle from '@site/src/components/PageTitle';

# SMOVE

<PageTitle title="Redis SMOVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SMOVE` command in Redis is used to move a member from one set to another. This is particularly useful when you need to atomically transfer an item between two sets, ensuring data consistency without having to remove from one set and add to another in separate operations.

## Syntax

```
SMOVE source destination member
```

## Parameter Explanations

- `source`: The key of the set where the member currently exists.
- `destination`: The key of the set to which the member will be moved.
- `member`: The specific element that needs to be transferred from the source set to the destination set.

## Return Values

- `(integer) 1` if the member was successfully moved.
- `(integer) 0` if the member was not present in the source set and no operation was performed.

## Code Examples

```cli
dragonfly> SADD set1 "one"
(integer) 1
dragonfly> SADD set1 "two"
(integer) 1
dragonfly> SADD set2 "three"
(integer) 1
dragonfly> SMOVE set1 set2 "one"
(integer) 1
dragonfly> SMOVE set1 set2 "one"
(integer) 0
dragonfly> SMEMBERS set1
1) "two"
dragonfly> SMEMBERS set2
1) "three"
2) "one"
```

## Best Practices

- Ensure that both source and destination keys exist and are of type set to prevent unexpected errors.

## Common Mistakes

- Attempting to move a member that does not exist in the source set will return 0 but will not throw an error. Always check the existence of the member in the source set if necessary.

## FAQs

### What happens if the source or destination keys don't exist?

If the `source` key does not exist, `SMOVE` returns 0 and no operation is performed. If the `destination` key does not exist, it is created automatically if the member is successfully moved.

### Can `SMOVE` be used with non-set keys?

No, both `source` and `destination` must be keys of type set. Using `SMOVE` with other data types will result in an error.
