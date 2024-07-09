---
description: Learn how to use Redis BF.MADD command to add one or more items to the Bloom filter.
---

import PageTitle from '@site/src/components/PageTitle';

# BF.MADD

<PageTitle title="Redis BF.MADD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BF.MADD` command in Redis is used with a Bloom Filter to add multiple elements at once. A Bloom Filter is a probabilistic data structure that provides an efficient way to test whether an element is a member of a set, at the cost of some false positives. This command is particularly useful for applications involving large datasets where space efficiency is critical, such as caching and web analytics.

## Syntax

```
BF.MADD <key> <element> [<element> ...]
```

## Parameter Explanations

- `<key>`: The name of the Bloom Filter.
- `<element>`: One or more elements to be added to the Bloom Filter. Multiple elements can be specified separated by spaces.

## Return Values

- An array of integers where each integer corresponds to whether the element was already present in the filter (0 for already present, 1 for newly added).

### Example Outputs:

- `[1, 1, 0]`: Indicates that the first and second elements were newly added, while the third element was already present.

## Code Examples

```cli
dragonfly> BF.RESERVE mybloom 0.01 1000
OK
dragonfly> BF.MADD mybloom "element1" "element2" "element3"
1) (integer) 1
2) (integer) 1
3) (integer) 1
dragonfly> BF.MADD mybloom "element1" "element4"
1) (integer) 0
2) (integer) 1
```

## Best Practices

- Ensure that you reserve your Bloom Filter with appropriate error rate and capacity using `BF.RESERVE` before using `BF.MADD`.
- Be mindful of the potential for false positives; the Bloom Filter can indicate that an element is present even if it is not.

## Common Mistakes

- Not reserving the Bloom Filter beforehand, which can lead to errors or inefficient storage.
- Misinterpreting the return values; a `0` means the element was already present, not that the operation failed.

## FAQs

### Can I use `BF.MADD` without reserving the filter first?

No, you must reserve the Bloom Filter with `BF.RESERVE` before adding elements. Otherwise, you may encounter errors or undefined behavior.

### What happens if I add the same element multiple times?

The first addition will return `1` indicating the element was added. Subsequent additions will return `0` showing that the element was already present in the filter.

### How do I control the accuracy of the Bloom Filter?

You can control the accuracy by setting the error rate and initial capacity when creating the Bloom Filter with `BF.RESERVE`.
