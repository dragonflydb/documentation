---
description: Learn how to use Redis PFADD command for adding elements to HyperLogLog data structure.
---

import PageTitle from '@site/src/components/PageTitle';

# PFADD

<PageTitle title="Redis PFADD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`PFADD` is a Redis command used to add elements to a HyperLogLog data structure. HyperLogLog is an algorithm that estimates the cardinality of a set, which means it can approximate the number of unique elements within the set. Use cases include counting unique visitors to a website, unique search queries, or any scenario where you need to count large numbers of distinct items efficiently.

## Syntax

```cli
PFADD key element [element ...]
```

## Parameter Explanations

- `key`: The name of the HyperLogLog structure.
- `element [element ...]`: One or more elements to be added to the HyperLogLog. You can pass multiple elements in a single command.

## Return Values

The command returns an integer:

- `(integer) 1` if at least one internal register was altered, meaning the HyperLogLog's state changed.
- `(integer) 0` if the HyperLogLog’s state was not altered by adding the elements.

## Code Examples

```cli
dragonfly> PFADD myhll "foo"
(integer) 1
dragonfly> PFADD myhll "bar" "baz"
(integer) 1
dragonfly> PFADD myhll "foo"
(integer) 0
dragonfly> PFCOUNT myhll
(integer) 3
```

## Best Practices

- Use `PFADD` with `PFCOUNT` to effectively manage and query HyperLogLog structures for estimating cardinalities.
- Remember, HyperLogLog is designed for approximations; use it when exact counts are less critical than memory efficiency.

## Common Mistakes

- Using HyperLogLog for scenarios requiring exact counts. HyperLogLog provides an estimate, not an exact number.
- Forgetting that `PFADD` can take multiple elements as arguments, which is useful for batch additions.

## FAQs

### How accurate is HyperLogLog?

HyperLogLog typically has a standard error rate of 0.81%, which is usually acceptable for most applications needing an approximate count.

### Can I retrieve the exact elements added to a HyperLogLog?

No, HyperLogLog only approximates the count of unique elements and does not store the actual elements.
