---
description:  Learn how to use Redis XREAD to read data from one or more streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XREAD

<PageTitle title="Redis XREAD Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XREAD` command is used to read data from one or more streams.
It is a blocking command by nature and is commonly utilized for implementing message queues, real-time data processing, and event sourcing patterns.

## Syntax

```shell
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
```

## Parameter Explanations

- `COUNT count`: The maximum number of entries to return per stream. Optional, defaults to return all available entries.
- `BLOCK milliseconds`: The maximum number of milliseconds the command will block if no messages are available. Optional, defaults to non-blocking behavior.
- `STREAMS key [key ...]`: One or more stream keys to read from.
- `ID [ID ...]`: One or more specific entry IDs to start reading from, or use `$` to start from the latest message.

## Return Values

The command returns a list of streams and the corresponding entries that were read from them, or an empty list if the `BLOCK` option is used and no messages are available within the specified time.

## Code Examples

### Basic Example

Read from a single stream starting from the first message:

```shell
dragonfly$> XADD mystream * name Alice age 30
"1609945144079-0"
dragonfly$> XADD mystream * name Bob age 25
"1609945144079-1"

dragonfly$> XREAD STREAMS mystream 0
1) 1) "mystream"
   2) 1) 1) "1609945144079-0"
         2) 1) "name"
            2) "Alice"
            3) "age"
            4) "30"
      2) 1) "1609945144079-1"
         2) 1) "name"
            2) "Bob"
            3) "age"
            4) "25"
```

### Using `XREAD` with `COUNT`

Read a limited number of entries from a stream:

```shell
dragonfly$> XREAD COUNT 1 STREAMS mystream 0
1) 1) "mystream"
   2) 1) 1) "1609945144079-0"
         2) 1) "name"
            2) "Alice"
            3) "age"
            4) "30"
```

### Using `XREAD` with Block Option

Block the command until new data arrives in the stream:

```shell
# Start a new terminal to add data after blocking
dragonfly$> XREAD BLOCK 2000 STREAMS mystream $
(null)

# In another terminal, add a new entry
dragonfly$> XADD mystream * name Charlie age 40
"1609945245092-0"

# Return to previous terminal and observe `XREAD` output
1) 1) "mystream"
   2) 1) 1) "1609945245092-0"
         2) 1) "name"
            2) "Charlie"
            3) "age"
            4) "40"
```

## Best Practices

- Consider using the `BLOCK` option to efficiently poll streams for new entries, reducing the need for constant querying.
- Use `COUNT` to prevent overwhelming your application with massive amounts of data if not necessary.

## Common Mistakes

- Overlooking the starting ID for the stream, which may result in missing entries if set incorrectly.
- Using blocking operations without a reasonable timeout can lead to application hangs if streams are quiet.

## FAQs

### What happens if a stream doesn't exist?

If a specified stream key does not exist, `XREAD` will not return entries from it and will move on to other specified streams.

### Can `XREAD` be used for multiple streams?

Yes, you can specify multiple streams to read simultaneously.
The command will return data from them in the specified order.