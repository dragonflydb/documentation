---
description: Learn how to use Redis ZSCAN command to incrementally iterate sorted sets elements and associated scores.
---

import PageTitle from '@site/src/components/PageTitle';

# ZSCAN

<PageTitle title="Redis ZSCAN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZSCAN` command in Redis is used to incrementally iterate over elements in a sorted set. This command is particularly useful for retrieving large sets of data without blocking the server, making it ideal for pagination or batch processing in real-time applications.

## Syntax

```plaintext
ZSCAN key cursor [MATCH pattern] [COUNT count]
```

## Parameter Explanations

- **key**: The name of the sorted set from which to retrieve elements.
- **cursor**: An integer that represents the iteration position. Initially set to 0, the cursor value is updated with each new call.
- **MATCH pattern**: (Optional) A pattern to filter the elements by their member names.
- **COUNT count**: (Optional) A hint about the number of elements to return per iteration.

## Return Values

The `ZSCAN` command returns an array containing two elements:

1. A new cursor, to be used in the next iteration.
2. An array of elements with their scores.

Example output:

```plaintext
1) "6"
2) 1) "member1"
   2) "1.0"
   3) "member2"
   4) "2.0"
```

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZSCAN myzset 0
1) "0"
2) 1) "one"
   2) "1"
   3) "two"
   4) "2"
   5) "three"
   6) "3"
dragonfly> ZSCAN myzset 0 MATCH t* COUNT 2
1) "0"
2) 1) "two"
   2) "2"
   3) "three"
   4) "3"
```

## Best Practices

- Use `MATCH` patterns to filter elements if you are only interested in specific members.
- Combine `COUNT` with your `ZSCAN` calls to balance between performance and completeness, especially when dealing with large datasets.

## Common Mistakes

- Not checking the returned cursor value properly, which can lead to incomplete iteration.
- Assuming `COUNT` is an exact limit; it’s merely a suggestion to Redis on how many elements should be returned.

## FAQs

### How do I know when the iteration is complete?

Iteration is complete when the cursor returned by `ZSCAN` is zero.

### Is `ZSCAN` guaranteed to return exactly `COUNT` elements?

No, `COUNT` is a suggestion to Redis; the actual number of returned elements might be slightly higher or lower.
