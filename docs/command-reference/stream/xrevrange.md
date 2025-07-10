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

- **Time complexity:** O(N) with N being the number of elements returned.
  If N is constant (e.g. always asking for the first 10 elements with `COUNT`), you can consider it O(1).
- **ACL categories:** @read, @stream, @slow

## Parameter Explanations

- `key`: The key of the stream from which elements are retrieved.
- `end`: The maximum ID of the stream entry to include in the output.
- `start`: The minimum ID of the stream entry to include in the output.
- `COUNT count` (optional): Limits the number of entries returned, fetching the first `count` elements in reverse order.

## Return Values

- The command returns a list of stream entries that correspond to the specified range.
- The entries are ordered from the highest ID to the lowest ID, within the specified range.
- Each entry is represented by a two-element array with the entry ID as the first element and the entry data (field-value pairs) as the second element.

## Code Examples

### Basic Example

Retrieve entries from a stream within a specified ID range in reverse order:

```shell
# Adding entries to a stream.
dragonfly$> XADD mystream * field1 value1
"1752105492073-0"

dragonfly$> XADD mystream * field2 value2
"1752105495609-0"

dragonfly$> XADD mystream * field3 value3
"1752105500367-0"

# Retrieve entries in reverse order.
dragonfly$> XREVRANGE mystream + -
1) 1) "1752105500367-0"
   2) 1) "field3"
      2) "value3"
2) 1) "1752105495609-0"
   2) 1) "field2"
      2) "value2"
3) 1) "1752105492073-0"
   2) 1) "field1"
      2) "value1"
```

### Using `COUNT` Option

You can get just the last element added into the stream using the `COUNT` option:

```shell
dragonfly$> XREVRANGE mystream + - COUNT 1
1) 1) "1752105500367-0"
   2) 1) "field3"
      2) "value3"
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

Stream IDs are lexicographic and do not support negative indexes.
