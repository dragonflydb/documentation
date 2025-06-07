---
description:  Learn how to use Redis XREVRANGE to fetch a range of messages from a stream in reverse order.
---

import PageTitle from '@site/src/components/PageTitle';

# XREVRANGE

<PageTitle title="Redis XREVRANGE Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XREVRANGE` command is used to return a range of elements from a stream in reverse order.
The directionality of this command makes it useful for scenarios where you need to process or display recent data entries before older ones, such as in messaging apps, event logging, or any application requiring reverse chronological order retrieval.

## Syntax

```shell
XREVRANGE key end start [COUNT count]
```

## Parameter Explanations

- `key`: The key of the stream from which elements are retrieved.
- `end`: The maximum ID of the stream entry to include in the output.
- `start`: The minimum ID of the stream entry to include in the output.
- `COUNT count` (optional): Limits the number of entries returned, fetching the first `count` elements in reverse order.

## Return Values

The command returns an array of entries, where each entry is itself an array consisting of an ID and a field-value pair list.
The entries are ordered from the highest ID to the lowest ID, within the specified range.

## Code Examples

### Basic Example

Retrieve entries from a stream within a specified ID range in reverse order:

```shell
# Adding entries to a stream.
dragonfly$> XADD mystream * field1 value1
"1617825600000-0"
dragonfly$> XADD mystream * field1 value2
"1617826800000-0"
dragonfly$> XADD mystream * field1 value3
"1617828000000-0"

# Retrieve entries in reverse order.
dragonfly$> XREVRANGE mystream 1617828000000-0 1617825600000-0
1) 1) "1617828000000-0"
   2) 1) "field1"
      2) "value3"
2) 1) "1617826800000-0"
   2) 1) "field1"
      2) "value2"
3) 1) "1617825600000-0"
   2) 1) "field1"
      2) "value1"
```

### Using `COUNT` Option

Retrieve a limited number of entries in reverse order using the `COUNT` option:

```shell
# Adding more entries to the stream.
dragonfly$> XADD mystream * field1 value4
"1617829200000-0"

# Retrieve only the two most recent entries.
dragonfly$> XREVRANGE mystream + - COUNT 2
1) 1) "1617829200000-0"
   2) 1) "field1"
      2) "value4"
2) 1) "1617828000000-0"
   2) 1) "field1"
      2) "value3"
```

### Applications in Event Logging

Consider a log stream where you want to fetch the most recent events up to a specific moment:

```shell
# Adding log entries.
dragonfly$> XADD logs * event login
"1617830000000-0"
dragonfly$> XADD logs * event logout
"1617831000000-0"

# Retrieve events in reverse order up to a specific ID.
dragonfly$> XREVRANGE logs 1617831000000-0 1617830000000-0
1) 1) "1617831000000-0"
   2) 1) "event"
      2) "logout"
2) 1) "1617830000000-0"
   2) 1) "event"
      2) "login"
```

## Best Practices

- Utilize `COUNT` to limit the number of entries returned, optimizing performance and reducing memory usage when processing large streams.
- Ensure that your specified `end` and `start` IDs correctly encapsulate the desired time or event window to avoid unexpected results.

## Common Mistakes

- Misinterpreting the order of `start` and `end`: since `XREVRANGE` operates in reverse, `end` should be greater than `start`.
- Overlooking the fact that stream IDs are ordered lexicographically, which can affect how ranges are defined and queried.

## FAQs

### What happens if the stream key does not exist?

If the stream key does not exist, `XREVRANGE` returns an empty array.

### Can negative indexes be used for `end` and `start` parameters?

Stream IDs are lexicographic and do not support negative indexes. Instead, ranges define specific or approximate position and order within the stream based on IDs.