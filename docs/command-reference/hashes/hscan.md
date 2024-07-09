---
description: "Learn how to use Redis HSCAN command to iteratively scan over a hash. Improve your data access strategy with this command."
---

import PageTitle from '@site/src/components/PageTitle';

# HSCAN

<PageTitle title="Redis HSCAN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HSCAN` command in Redis is used to incrementally iterate over the fields and values of a hash. This is particularly useful when dealing with large hashes that cannot be fetched entirely without blocking the server for a noticeable amount of time. Typical use cases include:

- Paginating through large datasets stored in a hash.
- Implementing background tasks that need to process records in chunks.

## Syntax

```cli
HSCAN key cursor [MATCH pattern] [COUNT count]
```

## Parameter Explanations

- `key`: The name of the hash from which to iterate.
- `cursor`: A position marker that represents the iteration state, typically starting at `0`.
- `MATCH pattern`: An optional parameter to filter the returned keys using glob-style patterns.
- `COUNT count`: An optional hint for the number of elements to return from the scan. It does not guarantee the number of results but attempts to approximate it.

## Return Values

The command returns an array of two elements:

1. **Cursor**: An updated cursor integer to be used in subsequent calls to continue the iteration.
2. **Elements**: An array containing the field and value pairs.

Example:

```cli
dragonfly> HSCAN myhash 0 MATCH f* COUNT 10
1) "4"
2) 1) "field1"
   2) "value1"
   3) "field2"
   4) "value2"
```

## Code Examples

```cli
dragonfly> HSET myhash field1 "value1" field2 "value2" field3 "value3"
(integer) 3
dragonfly> HSCAN myhash 0
1) "0"
2) 1) "field1"
   2) "value1"
   3) "field2"
   4) "value2"
   5) "field3"
   6) "value3"
dragonfly> HSCAN myhash 0 MATCH field*
1) "0"
2) 1) "field1"
   2) "value1"
   3) "field2"
   4) "value2"
   5) "field3"
   6) "value3"
dragonfly> HSCAN myhash 0 COUNT 2
1) "3"
2) 1) "field1"
   2) "value1"
   3) "field2"
   4) "value2"
```

## Best Practices

- Use `MATCH` to filter the results if you are only interested in specific patterns.
- Adjust the `COUNT` parameter based on your application's performance requirements and the size of the hash.

## Common Mistakes

- Forgetting to update the cursor for subsequent iterations. Always use the returned cursor to continue scanning.
- Assuming `COUNT` guarantees the exact number of items returned; it's an approximation, not a strict limit.

## FAQs

### How do I know when I've finished scanning?

When the cursor returned by `HSCAN` is `0`, the iteration is complete.

### Can I modify the hash while using HSCAN?

Yes, but modifications to the hash during iteration might affect the scan results. It's best to avoid changes to the hash until the scan is complete for consistent results.
