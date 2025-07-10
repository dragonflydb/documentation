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

- **Time complexity:** O(N) with N being the number of elements being returned.
  If N is constant (e.g. always asking for the first 10 elements with `COUNT`), you can consider it O(1).
- **ACL categories:** @read, @stream, @slow

## Parameter Explanations

- `key`: The key of the stream from which entries are fetched.
- `start` and `end`: The IDs that define the range of entries to retrieve.
  - Stream entry IDs follow the format `<timestamp>-<sequence>`, where both parts are 64-bit unsigned integers.
    The `timestamp` part represents the Unix time in milliseconds when the entry was added, and the `sequence` part is a unique incrementing number for entries added at the same timestamp.
  - **The IDs are inclusive by default.** Entries with IDs equal to `start` and `end` are included in the result if they exist.
  - To exclude the `start` or `end` entry, use the prefix `(` before the ID.
  - If only the `timestamp` part of `start` or `end` is provided to `XRANGE`:
    - The `sequence` number is set to the minimum value (i.e., `0`) for `start`.
    - The `sequence` number is set to the maximum value (i.e., `18446744073709551615`) for `end`.
  - Special IDs `-` and `+` represent the minimum and maximum possible IDs in the stream, respectively.
- `COUNT count` (optional): Limits the number of entries returned to `count`.

## Return Values

- The command returns a list of stream entries that correspond to the specified range.
- Each entry is represented by a two-element array with the entry ID as the first element and the entry data (field-value pairs) as the second element.

## Code Examples

### Retrieving Entries

We can retrieve entries from a stream in different ways:

```shell
# Adding entries to a stream.
dragonfly$> XADD mystream "1609459200000-0" sensor 0 temperature 23.0 humidity 50.0
"1609459200000-0"

dragonfly$> XADD mystream "1609459200001-0" sensor 1 temperature 23.1 humidity 50.1
"1609459200001-0"

dragonfly$> XADD mystream "1609459200001-1" sensor 2 temperature 23.2 humidity 50.2
"1609459200001-1"

dragonfly$> XADD mystream "1609459200002-0" sensor 3 temperature 23.3 humidity 50.3
"1609459200002-0"

# Retrieving entries using the first and second IDs from previous commands.
# Note that the start and end IDs are inclusive by default.
dragonfly$> XRANGE mystream "1609459200000-0" "1609459200001-0"
1) 1) "1609459200000-0"
   2) 1) "sensor"
      2) "0"
      3) "temperature"
      4) "23.0"
      5) "humidity"
      6) "50.0"
2) 1) "1609459200001-0"
   2) 1) "sensor"
      2) "1"
      3) "temperature"
      4) "23.1"
      5) "humidity"
      6) "50.1"

# Using the '(' prefix to exclude the end range entry.
dragonfly$> XRANGE mystream "1609459200000-0" "(1609459200001-0"
1) 1) "1609459200000-0"
   2) 1) "sensor"
      2) "0"
      3) "temperature"
      4) "23.0"
      5) "humidity"
      6) "50.0"

# Retrieving entries using only the timestamp part of the IDs.
# For the start ID, the sequence number is set to the minimum value.
# For the end ID, the sequence number is set to the maximum value.
# The command below is equivalent to: XRANGE mystream "1609459200000-0" "1609459200001-18446744073709551615"
dragonfly$> XRANGE mystream "1609459200000" "1609459200001"
1) 1) "1609459200000-0"
   2) 1) "sensor"
      2) "0"
      3) "temperature"
      4) "23.0"
      5) "humidity"
      6) "50.0"
2) 1) "1609459200001-0"
   2) 1) "sensor"
      2) "1"
      3) "temperature"
      4) "23.1"
      5) "humidity"
      6) "50.1"
3) 1) "1609459200001-1"
   2) 1) "sensor"
      2) "2"
      3) "temperature"
      4) "23.2"
      5) "humidity"
      6) "50.2"

# Retrieving all entries from the stream.
# Be cautious with this command as it can return a large amount of data.
dragonfly$> XRANGE mystream - +
# All entries in the stream are returned.
```

### Using the `COUNT` Option

The `COUNT` option can be used to limit the number of entries returned.
It can be combined with other parameters to control the amount of data fetched, which is helpful for iterating over large streams.

```shell
# Adding entries to a stream.
dragonfly$> XADD mystream "1609459200000-0" sensor 0 temperature 23.0 humidity 50.0
"1609459200000-0"

dragonfly$> XADD mystream "1609459200001-0" sensor 1 temperature 23.1 humidity 50.1
"1609459200001-0"

dragonfly$> XADD mystream "1609459200001-1" sensor 2 temperature 23.2 humidity 50.2
"1609459200001-1"

dragonfly$> XADD mystream "1609459200002-0" sensor 3 temperature 23.3 humidity 50.3
"1609459200002-0"

# Retrieving from the stream with the 'COUNT' option.
dragonfly$> XRANGE mystream - + COUNT 2
1) 1) "1609459200000-0"
   2) 1) "sensor"
      2) "0"
      3) "temperature"
      4) "23.0"
      5) "humidity"
      6) "50.0"
2) 1) "1609459200001-0"
   2) 1) "sensor"
      2) "1"
      3) "temperature"
      4) "23.1"
      5) "humidity"
      6) "50.1"
```

## Best Practices

- Using the `COUNT` option can help limit the amount of data transferred and improve performance for large streams.
- Use precise `start` and `end` IDs to avoid retrieving unnecessary entries and to maintain efficient operations.

## Common Mistakes

- Providing `start` or `end` in incorrect formats leads to errors.
- Providing `start` and `end` IDs in the wrong order can result in empty responses.

## FAQs

### What happens if the stream key does not exist?

If the stream key does not exist, `XRANGE` returns an empty list.

### How are stream IDs formatted?

Stream entry IDs are formatted as `<timestamp>-<sequence>`, where the `timestamp` part represents the Unix time in milliseconds when the entry was added,
and the `sequence` part is a unique incrementing number for entries added at the same timestamp.
When adding an entry, you can also specify the ID yourself instead of using `*`, but it must be unique and incrementing.
