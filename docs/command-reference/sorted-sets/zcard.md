---
description: Learn to use Redis ZCARD command to get the total number of elements in a sorted set.
---

import PageTitle from '@site/src/components/PageTitle';

# ZCARD

<PageTitle title="Redis ZCARD Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

The `ZCARD` command is used in Redis to get the number of members in a sorted set. This is particularly useful when you need to determine the size of a sorted set without retrieving all its values, which can be helpful for optimizing performance or managing data structures where the count of elements matters.

## Syntax

```plaintext
ZCARD key
```

## Parameter Explanations

- **key**: This is the name of the sorted set. It is a required parameter. The key must reference an existing sorted set; otherwise, the command will return 0.

## Return Values

- **Integer reply**: Returns the number of elements in the sorted set. If the key does not exist, it returns 0.

### Example:

If `myzset` contains three elements:

```cli
dragonfly> ZCARD myzset
(integer) 3
```

If `myzset` does not exist:

```cli
dragonfly> ZCARD myzset
(integer) 0
```

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZCARD myzset
(integer) 3
dragonfly> DEL myzset
(integer) 1
dragonfly> ZCARD myzset
(integer) 0
```

## Best Practices

- **Memory Efficiency**: Use `ZCARD` to check the number of elements before performing operations that depend on the size of the sorted set.

## Common Mistakes

- **Key Not Existing**: Assuming that `ZCARD` will return an error if the key does not exist. It actually returns 0.
- **Wrong Data Type**: Using `ZCARD` on keys that are not sorted sets. This will result in an error.

## FAQs

### What happens if I use `ZCARD` on a non-sorted set key?

You will receive an error indicating that the key holds the wrong kind of value because `ZCARD` only works with sorted sets.

### Can `ZCARD` be used to check the existence of a sorted set?

Yes, indirectly. If `ZCARD` returns 0, the sorted set either does not exist or is empty. To explicitly check for existence, you might prefer using the `EXISTS` command.
