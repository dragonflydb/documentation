---
description: Learn how to use Redis XRANGE to retrieve a range of messages from a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XRANGE

<PageTitle title="Redis XRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XRANGE` command is used to retrieve a range of entries from a Redis stream. It is useful for accessing entries in an ordered, chronological sequence, which is typical in event logging, messaging systems, or any time-series data.

## Syntax

```plaintext
XRANGE key start end [COUNT count]
```

## Parameter Explanations

- `key`: The name of the stream.
- `start`: The minimum ID to start the range (inclusive). Use `-` to represent the smallest possible ID.
- `end`: The maximum ID to end the range (inclusive). Use `+` to represent the largest possible ID.
- `[COUNT count]`: Optional. Limits the number of entries returned.

## Return Values

The command returns an array where each element is another array representing an entry. Each entry array contains:

- The entry ID.
- A sub-array of field-value pairs for that entry.

### Example

```plaintext
dragonfly> XRANGE mystream - +
1) 1) "1609459200001-0"
   2) 1) "field1"
      2) "value1"
2) 1) "1609459200002-0"
   2) 1) "field2"
      2) "value2"
```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1609459200001-0"
dragonfly> XADD mystream * field2 value2
"1609459200002-0"
dragonfly> XRANGE mystream - +
1) 1) "1609459200001-0"
   2) 1) "field1"
      2) "value1"
2) 1) "1609459200002-0"
   2) 1) "field2"
      2) "value2"
dragonfly> XRANGE mystream - + COUNT 1
1) 1) "1609459200001-0"
   2) 1) "field1"
      2) "value1"
```

## Best Practices

- When using `XRANGE` on large streams, the `COUNT` option can help limit the amount of data transferred, improving performance.

## Common Mistakes

- Omitting either `start` or `end` will result in a syntax error.
- Using invalid IDs for `start` or `end` will not return the correct results.

## FAQs

### What does `-` and `+` signify in `XRANGE`?

`-` signifies the smallest possible ID, and `+` signifies the largest possible ID, effectively allowing you to cover the full range of the stream.

### Can I use `XRANGE` to get entries in reverse order?

No, `XRANGE` retrieves entries in the natural ascending order. To get entries in reverse, use `XREVRANGE`.
