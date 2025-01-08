---
description:  Learn how to use Redis XLEN to get the length of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XLEN

<PageTitle title="Redis XLEN Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XLEN` command is used to determine the number of entries in a stream.
It is particularly useful for monitoring and managing data streams, providing quick insights into the size and health of your data pipeline.

## Syntax

```shell
XLEN key
```

## Parameter Explanations

- `key`: The key of the stream for which you wish to know the number of entries.

## Return Values

The command returns the number of entries (as an integer) currently present in the specified stream.

## Code Examples

### Basic Example

Determine the number of entries in a stream:

  
```shell
dragonfly$> XADD mystream * sensor-temperature 23.1
"1678819562090-0"
dragonfly$> XADD mystream * sensor-humidity 60
"1678819562091-0"
dragonfly$> XADD mystream * sensor-temperature 22.8
"1678819562092-0"
dragonfly$> XLEN mystream
(integer) 3
```

### Handling a Non-existent Stream

Check the length of a non-existent stream:

  
```shell
dragonfly$> XLEN nonexistent_stream
(integer) 0
```

### Using `XLEN` in Monitoring

Consider using `XLEN` as part of a monitoring solution to track the number of events in a stream at any point in time:

  
```shell
dragonfly$> XADD events * user-login user123
"1678819562093-0"
dragonfly$> XADD events * user-logout user123
"1678819562094-0"
dragonfly$> XLEN events
(integer) 2
# Use this value to monitor activity levels or detect anomalies in the number of events.
```

## Best Practices

- Integrate `XLEN` into your monitoring dashboards to provide real-time feedback on stream sizes and help detect bottlenecks or unusual activity patterns.
- Regularly check stream lengths as part of a comprehensive data management strategy.

## Common Mistakes

- Using `XLEN` on non-stream data types will result in an error, so ensure that the key provided is indeed a stream.
- Confusing `XLEN` with list length commands like `LLEN`, as they apply to different data structures.

## FAQs

### What happens if the key does not exist?

If the key does not exist or is not of stream type, `XLEN` returns `0`.

### Can `XLEN` be used to determine entries in other data types like lists or sets?

No, `XLEN` is specifically designed for streams.
To determine the length of other data types, use the appropriate commands such as `LLEN` for lists or `SCARD` for sets.