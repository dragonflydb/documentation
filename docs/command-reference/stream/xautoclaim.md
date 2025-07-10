---
description:  Learn how to use Redis XAUTOCLAIM to help with message recovery, claiming pending messages from other consumers.
---

import PageTitle from '@site/src/components/PageTitle';

# XAUTOCLAIM

<PageTitle title="Redis XAUTOCLAIM Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XAUTOCLAIM` command is used within the context of streams for effectively managing pending messages.
The command transfers ownership of pending stream messages from one consumer to another,
which is particularly useful in scenarios where message processing needs to be resilient and messages shouldn't remain stuck with unavailable consumers.
`XAUTOCLAIM` works like using [`XPENDING`](xpending.md) followed by [`XCLAIM`](xclaim.md) but offers a simpler way to handle message delivery failures with [`SCAN`](../generic/scan.md)-like behavior.

## Syntax

```shell
XAUTOCLAIM key group consumer min-idle-time start [COUNT count] [JUSTID]
```

- **Time complexity:** O(1) if `COUNT` is small.
- **ACL categories:** @write, @stream, @fast

## Parameter Explanations

- `key`: The key of the stream.
- `group`: The consumer group name.
- `consumer`: The new owner consumer for the pending messages.
- `min-idle-time`: Minimum idle time (in milliseconds) for a message to be claimed.
- `start`: The ID from which to start scanning for potential messages to claim.
- `COUNT count` (optional): Limit the number of messages to claim in a single call.
- `JUSTID` (optional): If specified, only message IDs are returned, not the messages themselves.

## Return Values

The command returns a three-element array:

- A stream entry ID for the next `XAUTOCLAIM` call. **Note that a returned ID of `0-0` means the entire stream was scanned.**
- An array of successfully claimed messages, formatted the same as the response of [`XRANGE`](xrange.md).
- An array of message IDs that no longer exist in the stream, and were deleted from the PEL in which they were found.

## Code Examples

### Basic Example

Claim messages that have been pending for over 5 seconds:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $ MKSTREAM
OK

dragonfly$> XADD mystream * name Alice
"1636581234567-0"

dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1636581234567-0"
         2) 1) "name"
            2) "Alice"

# Assume 'consumer-1' is unavailable and 'consumer-2' takes over.
dragonfly$> XAUTOCLAIM mystream mygroup consumer-2 5000 0
1) "0-0" # Next ID to scan from. Note that '0-0' means the entire stream was scanned.
2) 1) 1) "1736363819856-0"
      2) 1) "name"
         2) "Alice"
3) (empty array)
```

### Using `XAUTOCLAIM` with `COUNT` Option

Claim up to 2 messages pending beyond 2 seconds:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $ MKSTREAM
OK

dragonfly$> XADD mystream * name Alice
"1736363098647-0"

dragonfly$> XADD mystream * name Bob
"1736363102426-0"

dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 2 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1736363098647-0"
         2) 1) "name"
            2) "Alice"
      2) 1) "1736363102426-0"
         2) 1) "name"
            2) "Bob"

dragonfly$> XAUTOCLAIM mystream mygroup consumer-2 2000 0 COUNT 2
1) "0-0" # Next ID to scan from. Note that '0-0' means the entire stream was scanned.
2) 1) 1) "1736363098647-0"
      2) 1) "name"
         2) "Alice"
   2) 1) "1736363102426-0"
      2) 1) "name"
         2) "Bob"
3) (empty array)
```

## Best Practices

- Regularly use `XAUTOCLAIM` to prevent pending messages from being stuck with unavailable consumers.
- Utilize the `JUSTID` option when only message identifiers are needed, reducing network load.
- Setting a sensible `COUNT` can optimize performance by not overloading the consumer with too many messages at once.

## Common Mistakes

- Not correctly setting the `min-idle-time`, leading to unclaimed or incorrectly claimed messages.
- Forgetting to create the consumer group beforehand, as `XAUTOCLAIM` requires an existing consumer group.

## FAQs

### What happens if there are no messages to claim?

If there are no messages pending or meeting the criteria, an empty array is returned.

### Can I claim messages with a `min-idle-time` of zero?

Yes, but an idle time of zero means messages are immediately available for claiming, often unsuitable for normal operations where consumers might be briefly unavailable.
