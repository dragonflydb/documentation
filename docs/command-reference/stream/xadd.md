---
description:  Learn how to use Redis XADD to append a new entry to a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XADD

<PageTitle title="Redis XADD Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XADD` command is used to append a new entry to a stream. 
Streams are data structures that enable storing and processing ordered logs of events, and `XADD` is essential for adding data to these streams.

## Syntax

```shell
XADD key [MAXLEN ~ count] * field value [field value ...]
```

## Parameter Explanations

- `key`: The key of the stream where the entry will be appended.
- `MAXLEN ~ count` (optional): A flag to cap the length of the stream to `count` items; `~` is used to approximate trimming, making it more efficient.
- `*`: Automatically assigns an ID that includes the current milliseconds timestamp and an incrementing sequence number.
- `field value`: Pairs of field names and their corresponding values, forming the data within the entry.

## Return Values

The command returns the unique ID of the added stream entry, a string representing the timestamp and sequence number.

## Code Examples

### Basic Example

Add an entry to a stream:

```shell
dragonfly> XADD mystream * sensor-id 1234 temperature 19.8
"1609459200001-0"
```

### Limit Stream Length

Add an entry and trim the stream to keep only the latest 5 entries:

```shell
dragonfly> XADD mystream MAXLEN ~ 5 * sensor-id 1235 temperature 20.1
"1609459200002-0"
```

### Add Multiple Field-Value Pairs

Stream entries can contain multiple field-value pairs:

```shell
dragonfly> XADD mystream * sensor-id 1236 temperature 20.3 humidity 40
"1609459200003-0"
```

## Best Practices

- Use the `MAXLEN` parameter to manage stream size, especially when operating under memory constraints.
- Ensure field names are consistent in the stream structure to simplify data processing downstream.
- When storing multiple data points, structure entries as time-stamped records for better traceability.

## Common Mistakes

- Providing an odd number of arguments results in a syntax error, as entries must consist of field-value pairs.
- Not using the `*` for the ID will require manually assigning unique IDs, which can be error-prone.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `XADD` will automatically create a new stream with the specified entry.

### Can I use specific IDs instead of `*`?

Yes, you can specify your own unique ID instead of using `*`, but you must ensure it is unique and greater than the last entry's ID.