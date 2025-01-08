---
description:  Learn how to use Redis XRANGE to retrieve a range of messages from a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XRANGE

<PageTitle title="Redis XRANGE Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XRANGE` command is used to return a range of elements in a stream.
Streams are powerful data types for handling ordered logs and time-series data, making `XRANGE` especially useful for retrieving entries within specified time frames or other ranges.

## Syntax

```shell
XRANGE key start end [COUNT count]
```

## Parameter Explanations

- `key`: The key of the stream from which entries are fetched.
- `start`: The minimum ID of the range, inclusive.
- `end`: The maximum ID of the range, inclusive.
- `COUNT count` (optional): Limits the number of entries returned to 'count'.

## Return Values

The command returns a list of stream entries that correspond to the specified range.
Each entry is represented by a two-element array with an ID and a subsequent map of field-value pairs.

## Code Examples

### Basic Example

Retrieve all entries within a specified range:

```shell
# Adding entries to the stream
dragonfly$> XADD mystream * foo "1" bar "data1"
"1609459200000-0"
dragonfly$> XADD mystream * foo "2" bar "data2"
"1609459200010-0"

# Retrieving entries from '1609459200000-0' to '1609459200010-0'
dragonfly$> XRANGE mystream 1609459200000-0 1609459200010-0
1) 1) "1609459200000-0"
   2) 1) "foo"
      2) "1"
      3) "bar"
      4) "data1"
2) 1) "1609459200010-0"
   2) 1) "foo"
      2) "2"
      3) "bar"
      4) "data2"
```

### Using `COUNT` Option

Retrieve a limited number of entries starting from a specific ID:

```shell
# Adding another entry
dragonfly$> XADD mystream * foo "3" bar "data3"
"1609459200020-0"

# Retrieve only one entry starting from '1609459200000-0'
dragonfly$> XRANGE mystream 1609459200000-0 1609459200020-0 COUNT 1
1) 1) "1609459200000-0"
   2) 1) "foo"
      2) "1"
      3) "bar"
      4) "data1"
```

## Best Practices

- When processing large streams, using the `COUNT` parameter can help limit the amount of data transferred and improve performance.
- Use precise `start` and `end` IDs to avoid retrieving unnecessary entries and to maintain efficient operations.

## Common Mistakes

- Providing `start` or `end` in incorrect formats can lead to errors; ensure the IDs follow the correct stream ID format (e.g., `<timestamp>-<sequence>`).
- Not specifying an `end` range if the intent is to read bounded data. Omitting this parameter leads to fetching entries up to the maximum sequence for the start's timestamp.

## FAQs

### What happens if the stream key does not exist?

If the stream key does not exist, `XRANGE` returns an empty list.

### How are stream IDs formatted?

Stream IDs are formatted as `<milliseconds-time>-<sequence-number>`, where the sequence number starts at zero and increases with each entry at the same timestamp.