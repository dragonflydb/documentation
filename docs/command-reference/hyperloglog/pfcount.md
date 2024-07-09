---
description: Learn how to use Redis PFCOUNT command to get an estimated count of unique elements.
---

import PageTitle from '@site/src/components/PageTitle';

# PFCOUNT

<PageTitle title="Redis PFCOUNT Explained (Better Than Official Docs)" />

"## Introduction and Use Case(s)

PFCOUNT is a Redis command used to count the unique elements in a HyperLogLog data structure. This command is particularly useful for large-scale counting scenarios where an approximate result is acceptable, such as tracking unique visitors to a website, counting distinct items in a large dataset, or estimating the cardinality of big data streams.

## Syntax

```plaintext
PFCOUNT key [key ...]
```

## Parameter Explanations

- `key`: The name of the HyperLogLog data structure from which the unique count is requested. Multiple keys can be provided, in which case the estimated cardinality is calculated for the merged HyperLogLog structures.

## Return Values

The PFCOUNT command returns an integer that represents the approximate number of distinct elements observed via the specified HyperLogLog structures.

### Examples:

1. When querying a single key:

   ```cli
   dragonfly> PFADD hll myelement
   (integer) 1
   dragonfly> PFCOUNT hll
   (integer) 1
   ```

2. When querying multiple keys:
   ```cli
   dragonfly> PFADD hll1 element1
   (integer) 1
   dragonfly> PFADD hll2 element2
   (integer) 1
   dragonfly> PFCOUNT hll1 hll2
   (integer) 2
   ```

## Code Examples

### Example 1: Basic Usage with One Key

```cli
dragonfly> PFADD users user1 user2 user3
(integer) 1
dragonfly> PFCOUNT users
(integer) 3
```

### Example 2: Merging Multiple HyperLogLogs

```cli
dragonfly> PFADD page_views_1 visitor1 visitor2
(integer) 1
dragonfly> PFADD page_views_2 visitor2 visitor3
(integer) 1
dragonfly> PFCOUNT page_views_1 page_views_2
(integer) 3
```

## Best Practices

- Use PFCOUNT when you need to manage large volumes of data with the requirement of approximate distinct counts rather than exact values.
- Suitable scenarios include web analytics, IoT data aggregation, and event logging where counting individual occurrences would be computationally expensive.

## Common Mistakes

### Misunderstanding Precision

HyperLogLog provides an estimate, not an exact count. Relying on it for applications needing precise counts may lead to inaccuracies.

### Incorrect Key Usage

Using non-HyperLogLog keys with PFCOUNT will result in errors. Ensure the keys provided have been initialized with HyperLogLog commands like PFADD.

## FAQs

### Why should I use PFCOUNT instead of a simple SET to count unique elements?

PFCOUNT uses significantly less memory compared to a SET for counting unique elements, especially when dealing with millions of entries. This trade-off comes at the cost of slight precision loss.

### Can PFCOUNT return incorrect results?

While PFCOUNT is designed to provide approximate counts with high accuracy, it is not exact. The margin of error is typically low but present.
