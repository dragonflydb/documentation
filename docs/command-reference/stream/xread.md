---
description:  Learn how to use Redis XREAD to read data from one or more streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XREAD

<PageTitle title="Redis XREAD Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XREAD` command is used to read data from one or more streams.
It is a blocking command by nature and is commonly utilized for implementing message queues, real-time data processing, and event sourcing patterns. When used as non-blocking, `XREAD` is more suited in order to consume the stream starting from the first entry which is greater than any other entry we saw so far. So what we pass to `XREAD` in this case is, for each stream, the ID of the last element that we received from that stream.

## Syntax

```shell
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] id [id ...]
```

- **Time complexity:** 
- **ACL categories:** @read, @stream, @slow, @blocking

## Parameter Explanations

- `COUNT count`: The maximum number of entries to return per stream. Optional, defaults to return all available entries.
- `BLOCK milliseconds`: The maximum number of milliseconds the command will block if no messages are available. Optional, defaults to non-blocking behavior.
- `STREAMS key`: One or more stream keys to read from.
- `id`: One or more specific entry IDs to start reading from, or use `$` to start from the latest message.

## Return Values

- The command returns a list of streams and the corresponding entries that were read from them.
- If the `BLOCK` option is used and a timeout occurs, or if there is no stream that can be served, `nil` is returned.

## Code Examples

### Basic Example

Read from a single stream starting from the first message (non-blocking):

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

Read a limited number of entries from a stream (non-blocking):

```shell
dragonfly$> XADD mystream * name Alice age 30
"1752099700000-0"

dragonfly$> XADD mystream * name Bob age 25
"1752099799999-0"

# Read 1 entry from the beginning.
# Note that '0' is an incomplete ID, which is equivalent to '0-0' in this case.
dragonfly$> XREAD COUNT 1 STREAMS mystream 0
1) 1) "mystream"
   2) 1) 1) "1752099700000-0"
         2) 1) "name"
            2) "Alice"
            3) "age"
            4) "30"

# Read 1 entry after the ID "1752099700000-0".
dragonfly$> XREAD COUNT 1 STREAMS mystream "1752099700000-0"
1) 1) "mystream"
   2) 1) 1) "1752099799999-0"
         2) 1) "name"
            2) "Bob"
            3) "age"
            4) "25"
```

### Reading from Multiple Streams

Read a limited number of entries from multiple streams (non-blocking):

```shell
dragonfly$> XADD mystream1 * name Alice age 30
"1752100089353-0"

dragonfly$> XADD mystream1 * name Bob age 25
"1752100097545-0"

dragonfly$> XADD mystream2 * name Charlie age 20
"1752100108387-0"

dragonfly$> XREAD COUNT 1 STREAMS mystream1 mystream2 "0-0" "0-0"
1) 1) "mystream1"
   2) 1) 1) "1752100089353-0"
         2) 1) "name"
            2) "Alice"
            3) "age"
            4) "30"
2) 1) "mystream2"
   2) 1) 1) "1752100108387-0"
         2) 1) "name"
            2) "Charlie"
            3) "age"
            4) "20"
```

### Using `XREAD` with the `BLOCK` Option

Block the command until new data arrives in the stream:

```shell
# In a client terminal, set up a blocking read for 20 seconds.
dragonfly$> XREAD BLOCK 20000 STREAMS mystream $
```

```shell
# In a new client terminal, within 20 seconds, add an entry to the stream.
dragonfly$> XADD mystream * name Charlie age 20
"1609945245092-0"
```

```shell
# Return to first client terminal and observe `XREAD` output.
1) 1) "mystream"
   2) 1) 1) "1752100585277-0"
         2) 1) "name"
            2) "Charlie"
            3) "age"
            4) "20"
(1.23s) # Wait time.
```

When using the `BLOCK` option, sometimes we want to receive just entries that are added to the stream via `XADD` starting from the moment we block. In such a case we are not interested in the history of already added entries. For this use case, we would have to check the stream top entry ID, and use such ID in the `XREAD` command line. This is not clean and requires to call other commands, so instead it is possible to use the special `$` ID to signal the stream that we want only the new entries.

It is very important to understand that you should use the `$` ID only for the first call to `XREAD`. Later the ID should be the one of the last reported item in the stream, otherwise you could miss all the entries that are added in between.

## Best Practices

- Consider using the `BLOCK` option to wait for streams for new entries, reducing the need for constant querying.
- Use `COUNT` to prevent overwhelming your application with massive amounts of data if not necessary.

## Common Mistakes

- Overlooking the starting ID for the stream, which may result in missing entries if set incorrectly.
- Using blocking operations without a reasonable timeout can lead to application hangs if streams are quiet.

## FAQs

### What happens if a stream doesn't exist?

If a specified stream key does not exist, `XREAD` will not return entries from it and will move on to other specified streams.
