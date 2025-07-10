---
description:  Learn how to use Redis XTRIM to limit the length of a stream to a certain size.
---

import PageTitle from '@site/src/components/PageTitle';

# XTRIM

<PageTitle title="Redis XTRIM Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XTRIM` command is used to manage the length of a stream by trimming entries.
It helps in controlling memory usage by removing old entries from the stream.
`XTRIM` can be useful for applications like logging, where recent data is more critical than historical data.

## Syntax

```shell
XTRIM key <MAXLEN | MINID> [= | ~] threshold [LIMIT count]
```

- **Time complexity:** O(N), with N being the number of evicted entries.
- **ACL categories:** @write, @stream, @slow

## Parameter Explanations

- `key`: The key of the stream that you want to trim.
- `MAXLEN`: Trims entries as long as the stream's length exceeds the specified `threshold` (a positive integer).
- `MINID`: Trims entries with IDs lower than `threshold` (a stream ID).
- `=`: Ensures the trimming is precisely executed to the specified threshold.
- `~`: Instructs the trimming operation to be **nearly exact** in order to improve performance.
- `threshold`: The threshold, which is the number of entries for `MAXLEN` or the entry ID for `MINID`.
- `LIMIT count`: Another way to control the amount of work done by the command when using the `~`, is the `LIMIT` clause.
  When used, it specifies the maximal count of entries that will be evicted.
  When `LIMIT count` is not specified, the default value of 100 * the number of entries in a macro node will be
  implicitly used as the count. Specifying the value `0` as `count` disables the limiting mechanism entirely.

By default, or when provided with the optional `=` argument, the command performs exact trimming.
Depending on the strategy, exact trimming means:

- `MAXLEN`: the trimmed stream's length will be exactly the minimum between its original length and `threshold`.
- `MINID`: the oldest ID in the stream will be exactly the maximum between its original oldest ID and `threshold`.

## Return Values

- The command returns the number of entries removed from the stream.

## Code Examples

### Using `MAXLEN` to Trim

Trim a stream to a maximum of three entries:

```shell
dragonfly$> XADD mystream * field1 value1
"1609459200000-0"

dragonfly$> XADD mystream * field2 value2
"1609459200001-0"

dragonfly$> XADD mystream * field3 value3
"1609459200002-0"

dragonfly$> XADD mystream * field4 value4
"1609459200003-0"

dragonfly$> XADD mystream * field5 value5
"1609459200004-0"

dragonfly$> XTRIM mystream MAXLEN 3
(integer) 2
```

### Using `MINID` to Trim

Remove all entries with IDs less than a specific timestamp:

```shell
dragonfly$> XADD mystream * field1 value1
"1609459200000-0"

dragonfly$> XADD mystream * field2 value2
"1609459200001-0"

dragonfly$> XADD mystream * field3 value3
"1609459200002-0"

dragonfly$> XTRIM mystream MINID "1609459200001-0"
(integer) 1
```

### Nearly Exact Trimming with `~`

Improve performance by approximating the trim operation:

```shell
dragonfly$> XADD mystream * field1 value1
"1609459200000-0"

dragonfly$> XADD mystream * field2 value2
"1609459200001-0"

dragonfly$> XADD mystream * field3 value3
"1609459200002-0"

dragonfly$> XADD mystream * field4 value4
"1609459200003-0"

dragonfly$> XADD mystream * field5 value5
"1609459200004-0"

dragonfly$> XTRIM mystream MAXLEN ~ 2
(integer) 0
```

## Best Practices

- Use approximative trimming with `~` for better performance on large streams, when precision is not critical.
- Regularly trim streams if your application generates a significant amount of data, to manage memory usage efficiently.

## Common Mistakes

- Confusing `MAXLEN` and `MINID`. `MAXLEN` specifies a count of entries, whereas `MINID` specifies an entry ID threshold.
- Not considering the trade-off between approximation (`~`) and precision (`=`) in terms of performance and accuracy.

## FAQs

### What happens if the stream is empty or the key does not exist?

If the stream is empty or the key does not exist, `XTRIM` returns `0` since no entries are removed.

### Can I use negative values for `threshold`?

No, the `threshold` value for `MAXLEN` must be a positive integers, and the `threshold` value for `MINID` must be a valid ID.
