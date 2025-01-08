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
XADD key [<MAXLEN | MINID> [~ | =] threshold] <* | id> field value [field value ...]
```

## Parameter Explanations

- `key`: The key of the stream where the entry will be appended.
- `MAXLEN` (optional): A flag to cap the length of the stream to `threshold` items.
- `MINID` (optional): A flag to trim the stream to keep only entries with IDs greater than `threshold`.
- For `MAXLEN` or `MINID`, one of the following operators can be used:
  - The `~` operator is used to trim approximately, which can be more efficient but may not be exact.
  - The `=` operator is used to trim exactly to the specified threshold.
- In order to specify a unique ID for the entry in the stream, use one of the following options.
  - `*`: Automatically generate an ID that includes a timestamp and a sequence number.
  - `id`: A unique incremental ID for the entry specified by your application.
  - Either way, the stored ID is a **string representing two 64-bit integers separated by a hyphen (`-`)**.
- `field value`: Pairs of field names and their corresponding values, forming the data within the entry.

## Return Values

- The command returns the unique ID of the added stream entry.
- If the ID is automatically generated, the first part is a Unix timestamp in milliseconds, and the second part is an incrementing sequence number distinguishing entries with the same timestamp.

## Code Examples

### Basic Example

Add an entry to a stream:

```shell
dragonfly$> XADD mystream * sensor-id 1234 temperature 20.1
"1609459200001-0"
```

### Limit Stream Length

Add an entry and trim the stream to keep only the latest 5 entries:

```shell
dragonfly$> XADD mystream MAXLEN = 5 * sensor-id 1235 temperature 20.1
"1609459200002-0"
```

### Add Multiple Field-Value Pairs

Stream entries can contain multiple field-value pairs:

```shell
dragonfly$> XADD mystream * sensor-id 1236 temperature 20.1 humidity 40
"1609459200003-0"
```

### Use Specific ID

Specify a unique ID for the stream entry.
The ID can be in a full format or a partial format as shown below.
When using a specific ID, ensure it is unique and greater than the target stream top item's ID.

```shell
# Using an auto-generated ID.
dragonfly$> XADD mystream * sensor-id 1237 temperature 20.1
"1735929311498-0"

# Using a specific ID in full format (timestamp-sequence).
dragonfly$> XADD mystream "1735929311498-1" sensor-id 1237 temperature 20.2
"1735929311498-1"

# Using a specific ID in partial format (timestamp only).
dragonfly$> XADD mystream "1735929311498-*" sensor-id 1237 temperature 20.3
"1735929311498-2"

# Using an ID that is less than the top item's ID will result in an error.
# In this case, the partial format ID is less than the top item's ID.
dragonfly$> XADD mystream "1700000000000-*" sensor-id 1237 temperature 20.4
(error) ERR The ID specified in XADD is equal or smaller than the target stream top item
```

## Best Practices

- Use the `MAXLEN` parameter to manage stream size, especially when operating under memory constraints.
- Ensure field names are consistent in the stream structure to simplify data processing downstream.
- When storing multiple data points, structure entries as time-stamped records for better traceability.

## Common Mistakes

- Providing an odd number of arguments for the field-value list results in a syntax error.
- Not using the `*` for the ID will require manually assigning unique IDs, which can be error-prone.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `XADD` will automatically create a new stream with the specified key and append the entry to it.

### Can I use specific IDs instead of `*`?

Yes, you can specify your own unique ID instead of using `*`, but you must ensure the new ID is unique and is greater than the target stream top item's ID.
