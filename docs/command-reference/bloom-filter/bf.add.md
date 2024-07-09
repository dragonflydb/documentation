---
description: Learn how to use Redis BF.ADD command to add an item to the Bloom filter.
---

import PageTitle from '@site/src/components/PageTitle';

# BF.ADD

<PageTitle title="Redis BF.ADD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

BF.ADD is a command in Redis Bloom, an extension of Redis that provides probabilistic data structures. The BF.ADD command is used to add an item to a Bloom Filter, which is a space-efficient probabilistic data structure designed to test whether an element is a member of a set. This command is typically used in scenarios where memory efficiency is critical, and some false positives are acceptable, such as caching, detecting duplicates, or preprocessing large datasets.

## Syntax

```plaintext
BF.ADD key item
```

## Parameter Explanations

- `key`: The name of the Bloom Filter to which the item should be added. If the filter does not exist, it will be created.
- `item`: The item to add to the Bloom Filter. This can be any string value.

## Return Values

The command returns an integer:

- `(integer) 1` if the item was not previously present in the Bloom Filter.
- `(integer) 0` if the item was already present in the Bloom Filter.

## Code Examples

```cli
dragonfly> BF.ADD mybloom "hello"
(integer) 1
dragonfly> BF.ADD mybloom "world"
(integer) 1
dragonfly> BF.ADD mybloom "hello"
(integer) 0
```

## Best Practices

- Use Bloom Filters when you need to quickly determine membership with a low error rate and minimal memory footprint.
- Keep in mind that Bloom Filters can have false positives but never false negatives; this means they may tell you an item is in the set when it's not, but if they say an item is not in the set, it definitely isn't.

## Common Mistakes

- Overestimating the accuracy: The probability of false positives increases with the number of items added. Properly configure the size and hash functions of your Bloom Filter based on expected usage.
- Forgetting that there's no way to remove items from a standard Bloom Filter. If you need to remove items, consider using Counting Bloom Filters.

### How does the size of the Bloom Filter affect performance?

A larger Bloom Filter reduces the likelihood of false positives but consumes more memory. It's crucial to balance between acceptable false positive rates and memory usage.

### Can I use BF.ADD with non-string items?

BF.ADD is designed for string values. For non-string items, convert them to strings before adding them to the Bloom Filter.
