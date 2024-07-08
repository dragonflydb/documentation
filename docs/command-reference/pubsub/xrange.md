---
description: Learn how to use Redis XRANGE to retrieve a range of messages from a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XRANGE

<PageTitle title="Redis XRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XRANGE` is a Redis command used to read a range of entries from a stream. It's highly useful in scenarios where you need to process or monitor data streams, such as event logging, messaging systems, or real-time analytics.

## Syntax

```cli
XRANGE key start end [COUNT count]
```

## Parameter Explanations

- `key`: The name of the stream.
- `start`: The lower bound ID for the range (inclusive). Use `-` for the minimum possible ID.
- `end`: The upper bound ID for the range (inclusive). Use `+` for the maximum possible ID.
- `COUNT count` (optional): Limits the number of entries returned.

## Return Values

`XRANGE` returns an array of stream entries, each entry being an array itself containing the entry ID and field-value pairs. If no entries exist within the specified range, an empty array is returned.

Example outputs:

- When entries are found:
  ```cli
  1) 1) "1609459200000-0"
     2) 1) "field1"
        2) "value1"
        3) "field2"
        4) "value2"
  ```
- When no entries are found:
  ```cli
  (empty array)
  ```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1 field2 value2
"1609459200000-0"
dragonfly> XADD mystream * field1 value3 field2 value4
"1609459200001-0"
dragonfly> XRANGE mystream - +
1) 1) "1609459200000-0"
   2) 1) "field1"
      2) "value1"
      3) "field2"
      4) "value2"
2) 1) "1609459200001-0"
   2) 1) "field1"
      2) "value3"
      3) "field2"
      4) "value4"

dragonfly> XRANGE mystream 1609459200000-0 1609459200000-0
1) 1) "1609459200000-0"
   2) 1) "field1"
      2) "value1"
      3) "field2"
      4) "value2"

dragonfly> XRANGE mystream - + COUNT 1
1) 1) "1609459200000-0"
   2) 1) "field1"
      2) "value1"
      3) "field2"
      4) "value2"
```

## Best Practices

- Use `COUNT` to limit the number of entries returned, which can help manage memory and improve performance when working with large streams.

## Common Mistakes

- Specifying `start` greater than `end` will always return an empty array.
- Forgetting to use double quotes around IDs that include special characters like `-`.

## FAQs

### What happens if I specify an ID that doesn't exist?

The command will return entries with the closest higher IDs within the specified range.

### Is there a way to get only new entries added to the stream?

For this purpose, use the `XREAD` command instead, which is designed to block and wait for new entries.
