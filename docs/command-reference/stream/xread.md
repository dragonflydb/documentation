---
description: Learn how to use Redis XREAD to read data from one or more streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XREAD

<PageTitle title="Redis XREAD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XREAD` command is used to read data from one or multiple streams in Redis. It is commonly utilized in real-time data processing scenarios, where streams are used as logs or message queues. This command allows consumers to fetch new entries added to the streams since the last read, enabling efficient event streaming and data ingestion.

## Syntax

```plaintext
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
```

## Parameter Explanations

- `COUNT count`: Optional parameter that limits the number of entries returned per stream.
- `BLOCK milliseconds`: Optional parameter that makes the command block for a specified number of milliseconds if no data is available. If not specified, the command returns immediately with whatever data is available.
- `STREAMS key [key ...]`: Specifies the keys of the streams to read from.
- `ID [ID ...]`: Specifies the IDs from which to start reading in each respective stream. Use `$` to read only new messages.

## Return Values

The `XREAD` command returns an array, where each element represents a stream. Each stream element contains the stream name and an array of entries. Each entry consists of an ID and its corresponding fields and values.

Example:

```plaintext
1) 1) "mystream"
   2) 1) 1) "1625837942341-0"
         2) 1) "field1" 2) "value1" 3) "field2" 4) "value2"
      2) 1) "1625837942342-0"
         2) 1) "field1" 2) "value3" 3) "field2" 4) "value4"
```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1 field2 value2
"1625837942341-0"
dragonfly> XADD mystream * field1 value3 field2 value4
"1625837942342-0"
dragonfly> XREAD STREAMS mystream 0
1) 1) "mystream"
   2) 1) 1) "1625837942341-0"
         2) 1) "field1" 2) "value1" 3) "field2" 4) "value2"
      2) 1) "1625837942342-0"
         2) 1) "field1" 2) "value3" 3) "field2" 4) "value4"
```

## Best Practices

- **Use IDs efficiently**: When polling for new entries, use `$` for the ID to avoid re-reading old entries.
- **Handle blocking appropriately**: The `BLOCK` option should be used carefully to prevent high latencies in applications.

## Common Mistakes

- **Incorrect ID usage**: Specifying incorrect or non-sequential IDs can result in missing data or duplicate reads.
- **Not using COUNT with BLOCK**: Without `COUNT`, a blocked read might return too few entries than expected when data becomes available.

## FAQs

### How do I ensure I only read new entries?

Use `$` for the ID in the `XREAD` command to read only newly added entries.

### What happens if I don’t specify the `BLOCK` parameter?

If `BLOCK` is not specified, `XREAD` returns immediately with whatever data is available, potentially resulting in empty responses if there are no new entries.
