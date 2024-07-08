---
description: Learn how to incrementally iterate over a collection using Redis SSCAN command.
---

import PageTitle from '@site/src/components/PageTitle';

# SSCAN

<PageTitle title="Redis SSCAN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SSCAN` command in Redis is used to incrementally iterate over elements in a set. It is particularly useful for dealing with large sets without blocking the server, as it allows us to fetch small subsets of data at a time. Common scenarios include searching for specific elements within a large set or processing set elements in manageable chunks.

## Syntax

```plaintext
SSCAN key cursor [MATCH pattern] [COUNT count]
```

## Parameter Explanations

- **key**: The name of the set from which to iterate.
- **cursor**: An integer that represents the iteration state. To start iteration, set this to 0.
- **MATCH pattern** (optional): A pattern to filter the elements returned by the command.
- **COUNT count** (optional): A hint to the server about how many elements to return in each batch. The default is 10.

## Return Values

The `SSCAN` command returns an array with two elements:

1. The new cursor to be used in the next call.
2. An array of elements matching the given pattern (if any).

Example:

```plaintext
1) "4"
2) 1) "element1"
   2) "element2"
```

## Code Examples

```cli
dragonfly> SADD myset "one" "two" "three" "four" "five"
(integer) 5
dragonfly> SSCAN myset 0 MATCH "t*"
1) "4"
2) 1) "two"
   2) "three"
dragonfly> SSCAN myset 4 MATCH "t*"
1) "0"
2) (empty list or set)
```

## Best Practices

When using `SSCAN`, always check the returned cursor. If it returns "0," the iteration is complete. This approach ensures you do not miss any elements during the scan.

## Common Mistakes

- **Ignoring the cursor**: Not using the cursor returned by the previous `SSCAN` call leads to repetitive or incomplete scans.
- **Assuming COUNT is a hard limit**: The `COUNT` parameter is only a suggestion to Redis. It may return more or fewer than the specified number of elements.

## FAQs

### How does SSCAN differ from SMEMBERS?

`SMEMBERS` retrieves all elements of a set at once, which can be inefficient for large sets. `SSCAN` allows incremental retrieval, reducing memory overhead and avoiding potential server blockage.

### Can I use SSCAN in a multi-threaded environment?

Yes, but ensure each thread maintains its cursor state independently to avoid overlaps and ensure accurate scanning.
