---
description:  Learn how to use Redis XLEN to get the length of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XLEN

<PageTitle title="Redis XLEN Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XLEN` command is used to determine the number of entries in a stream.
The command is useful for monitoring and managing data streams, providing quick insights into the size and health of your data pipeline.

## Syntax

```shell
XLEN key
```

- **Time complexity:** O(1)
- **ACL categories:** @read, @stream, @fast

## Parameter Explanations

- `key`: The key of the stream for which you wish to know the number of entries.

## Return Values

- The command returns the number of entries in the specified stream as an integer.

## Code Examples

### Basic Example

Determine the number of entries in a stream:

```shell
dragonfly$> XADD mystream * sensor-1-temperature 23.1
"1678819562090-0"

dragonfly$> XADD mystream * sensor-2-temperature 23.2
"1678819562091-0"

dragonfly$> XADD mystream * sensor-3-temperature 23.3
"1678819562092-0"

dragonfly$> XLEN mystream
(integer) 3
```

### Non-Existent Stream

Check the length of a non-existent stream:

```shell
dragonfly$> XLEN non-existent-stream
(integer) 0
```

## Best Practices

- Regularly check stream lengths as part of a comprehensive data management strategy.
- Integrate `XLEN` into your monitoring dashboards to provide real-time feedback on stream sizes and help detect bottlenecks or unusual activity patterns.

## Common Mistakes

- Using `XLEN` on non-stream data types will result in an error, so ensure that the key provided is indeed a stream.
- Confusing `XLEN` with list length commands like `LLEN`, as they apply to different data structures.

## FAQs

### What happens if the stream key does not exist?

If the stream key does not exist, `XLEN` returns `0`.

### Can `XLEN` be used to determine entries in other data types like lists or sets?

No, `XLEN` is specifically designed for streams.
To determine the length of other data types, use the appropriate commands such as `LLEN` for lists or `SCARD` for sets.
