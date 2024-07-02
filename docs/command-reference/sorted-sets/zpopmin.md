---
description: Learn how to use the Redis ZPOPMIN command to remove and return the member with the lowest score in a sorted set, plus expert tips beyond the official docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZPOPMIN

<PageTitle title="Redis ZPOPMIN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZPOPMIN` command is used to remove and return the member with the lowest score from a sorted set. This is useful in scenarios where you need to process elements in ascending order of their scores, such as task scheduling or priority queues.

## Syntax

```plaintext
ZPOPMIN key [count]
```

## Parameter Explanations

- `key`: The name of the sorted set.
- `count` (optional): The number of elements to pop from the sorted set. If not provided, the default value is 1.

## Return Values

The command returns an array of the popped elements and their scores. If the optional count argument is provided, it returns up to `count` elements. For example:

- If no elements are in the sorted set, an empty array is returned.
- If the sorted set contains elements, it will return each element followed by its score.

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZPOPMIN myzset
1) "one"
2) "1"
dragonfly> ZPOPMIN myzset 2
1) "two"
2) "2"
3) "three"
4) "3"
dragonfly> ZPOPMIN myzset
(empty array)
```

## Best Practices

- Ensure the sorted set exists before calling `ZPOPMIN` to avoid unexpected empty results.
- Use the optional `count` parameter when you need to pop multiple elements at once to minimize the number of commands sent to the server.

## Common Mistakes

- Using `ZPOPMIN` on a non-existent key will return an empty array, which might be misinterpreted as there being no elements with low scores rather than the absence of the sorted set.
- Not providing the `count` parameter when intending to pop multiple elements can lead to multiple round-trip commands, which may affect performance.

## FAQs

### What happens if the sorted set is empty?

If the sorted set is empty, `ZPOPMIN` returns an empty array.

### Can I use `ZPOPMIN` to pop elements in descending order?

No, `ZPOPMIN` only removes elements with the lowest scores. To pop elements with the highest scores, use the `ZPOPMAX` command instead.
