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
XTRIM key [MAXLEN | MINID] [~ | =] threshold
```

## Parameter Explanations

- `key`: The key of the stream that you want to trim.
- `MAXLEN`: Trims the stream to ensure it does not exceed a specified number of entries.
- `MINID`: Trims entries with IDs less than a specified threshold.
- `~`: Approximates the trimming operation to improve performance.
- `=`: Ensures the trimming is precisely executed to the specified threshold.
- `threshold`: The maximum number of entries or the entry ID threshold.

## Return Values

The command returns the number of entries removed from the stream.

## Code Examples

### Basic MAXLEN Usage

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
dragonfly$> XTRIM mystream MAXLEN 3
(integer) 1
```

### Using MINID to Trim

Remove all entries with IDs less than a specific timestamp:

```shell
dragonfly$> XADD mystream * field1 value1
"1609459200000-0"
dragonfly$> XADD mystream * field2 value2
"1609459200001-0"
dragonfly$> XADD mystream * field3 value3
"1609459200002-0"
dragonfly$> XTRIM mystream MINID 1609459200001-0
(integer) 1
```

### Approximative Trimming with `~`

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
dragonfly$> XTRIM mystream MAXLEN ~ 2
(integer) 2
```

## Best Practices

- Use approximative trimming with `~` for better performance on large streams, when precision is not critical.
- Regularly trim streams if your application generates a significant amount of data, to manage memory usage efficiently.

## Common Mistakes

- Confusing `MAXLEN` and `MINID` — `MAXLEN` specifies a count of entries, whereas `MINID` specifies an entry ID threshold.
- Not considering the trade-off between approximation (`~`) and precision (`=`) in terms of performance and accuracy.

## FAQs

### What happens if the stream is empty or the key does not exist?

If the stream is empty or the key does not exist, `XTRIM` returns `0` since no entries are removed.

### Can I use negative indexes for `threshold`?

No, `threshold` values for both `MAXLEN` and `MINID` must be positive integers. Negative values are not applicable.