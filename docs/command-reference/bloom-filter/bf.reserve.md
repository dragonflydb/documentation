---
description: Learn how to use Redis BF.RESERVE to create a new Bloom filter entry in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# BF.RESERVE

<PageTitle title="Redis BF.RESERVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`BF.RESERVE` is a command used in Redis to create a Bloom filter with specified properties. A Bloom filter is a probabilistic data structure that is used to test whether an element is part of a set, with a possibility of false positives but no false negatives. This command is typically used in scenarios such as preventing spam, caching, and quickly determining set membership where space efficiency is critical.

## Syntax

```cli
BF.RESERVE <key> <error_rate> <capacity>
```

## Parameter Explanations

- `<key>`: The name of the key under which the Bloom filter will be stored.
- `<error_rate>`: The desired probability of false positives (e.g., 0.01 means 1%).
- `<capacity>`: The number of entries you expect to add to the filter.

## Return Values

The `BF.RESERVE` command returns a simple string reply:

- `OK`: Indicates that the Bloom filter was successfully created.

## Code Examples

```cli
dragonfly> BF.RESERVE mybloom 0.01 1000
"OK"
dragonfly> BF.RESERVE user_emails 0.001 5000
"OK"
```

## Best Practices

- Choose an appropriate error rate and capacity based on your use case requirements to balance between memory usage and accuracy.
- Monitor and possibly resize the Bloom filter if it becomes overfilled, as exceeding capacity can increase the false positive rate beyond the specified error rate.

## Common Mistakes

- Setting an overly low error rate might result in excessive memory consumption.
- Underestimating the capacity, which leads to higher than expected false positive rates if the actual number of items exceeds the specified capacity.

## FAQs

### How do I decide on an appropriate error rate?

The error rate should be chosen based on how acceptable false positives are for your application. Lower error rates reduce false positives but increase memory usage.

### What happens if I exceed the specified capacity?

Exceeding the specified capacity increases the likelihood of false positives. It is recommended to monitor your usage and consider resizing if necessary.
