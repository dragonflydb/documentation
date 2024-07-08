---
description: Learn how to use Redis XREVRANGE to fetch a range of messages from a stream in reverse order.
---

import PageTitle from '@site/src/components/PageTitle';

# XREVRANGE

<PageTitle title="Redis XREVRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XREVRANGE` is a Redis command used to retrieve entries from a stream in reverse order (from higher to lower IDs). This is particularly useful when you need to process recent events first or perform tasks such as log analysis starting from the most recent entries.

## Syntax

```plaintext
XREVRANGE key end start [COUNT count]
```

## Parameter Explanations

- **key**: The name of the stream.
- **end**: The maximum ID to start retrieving entries from, specified as a string. Use `+` for the latest entry.
- **start**: The minimum ID to stop retrieving entries at, specified as a string. Use `-` to indicate the earliest possible entry.
- **[COUNT count]**: Optional. Limits the number of entries returned to `count`. If not provided, all matching entries are returned.

## Return Values

The command returns an array of entries, where each entry is itself an array consisting of:

1. The entry ID.
2. An array of field-value pairs associated with that entry.

### Example Output

```plaintext
1) 1) "1609459200000-0"
   2) 1) "field1"
      2) "value1"
      3) "field2"
      4) "value2"
2) 1) "1609459199999-0"
   2) 1) "field1"
      2) "value1"
```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1 field2 value2
"1609459200000-0"

dragonfly> XADD mystream * field1 value3 field2 value4
"1609459200001-0"

dragonfly> XREVRANGE mystream + - COUNT 2
1) 1) "1609459200001-0"
   2) 1) "field1"
      2) "value3"
      3) "field2"
      4) "value4"
2) 1) "1609459200000-0"
   2) 1) "field1"
      2) "value1"
      3) "field2"
      4) "value2"
```

## Best Practices

- Utilize the `COUNT` option judiciously to avoid returning excessively large datasets, which can impact performance.
- Make sure to specify the appropriate `end` and `start` boundaries to focus on relevant data ranges.

## Common Mistakes

- Failing to correctly interpret the `end` and `start` parameters, especially when using the special characters `+` and `-`.
- Overlooking the use of `COUNT`, leading to potential performance issues with large streams.

## FAQs

### How do `end` and `start` parameters work in `XREVRANGE`?

The `end` parameter specifies the highest ID from which to start retrieving entries, while `start` indicates the lowest ID to retrieve. The command processes entries in reverse order, starting from `end` and stopping at `start`.

### Can I use `XREVRANGE` without specifying a `COUNT`?

Yes, if you omit the `COUNT` option, `XREVRANGE` will return all the entries between the specified `end` and `start`.
