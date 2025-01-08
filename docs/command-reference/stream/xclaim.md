---
description:  Learn how to use Redis XCLAIM to change the ownership of a pending message.
---

import PageTitle from '@site/src/components/PageTitle';

# XCLAIM

<PageTitle title="Redis XCLAIM Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XCLAIM` command is used to change the ownership of pending messages in a stream.
This is useful for scenarios such as distributed stream consumers where you need to handle message processing failures or reassignment of tasks to other consumers.

## Syntax

```shell
XCLAIM key group consumer min-idle-time id [id ...] [IDLE ms] [TIME ms-unix-time] 
       [RETRYCOUNT count] [FORCE] [JUSTID]
```

## Parameter Explanations

- `key`: The key of the stream.
- `group`: The consumer group name from which the pending messages are claimed.
- `consumer`: The new consumer name that will claim the pending message.
- `min-idle-time`: The minimum idle time (in milliseconds) that a message must have to be claimable.
- `id`: The ID(s) of the message(s) to be claimed; you can specify multiple IDs.
- `IDLE ms` (optional): Reassign the idle time to this value (in milliseconds).
- `TIME ms-unix-time` (optional): Use the specified Unix time for idle time calculation (useful for replication).
- `RETRYCOUNT count` (optional): Update the retry counter with the specified count.
- `FORCE` (optional): Claim the message even if it is not pending in the specified group.
- `JUSTID` (optional): Return just the message IDs without transferring message contents.

## Return Values

The command returns information about the claimed messages.
The result structure depends on whether `JUSTID` was used:

- Without `JUSTID`, it returns the entire message structure.
- With `JUSTID`, it only returns the IDs of the claimed messages.

## Code Examples

### Basic Example

Claim a specific pending message for a new consumer:

```shell
dragonfly$> XADD mystream * field1 value1
"1629392070655-0"

dragonfly$> XGROUP CREATE mystream mygroup 0
OK

# A consumer (i.e., 'consumer-1') reads the message, but does not acknowledge it yet.
# The message is now pending.
dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1629392070655-0"
         2) 1) "field1"
            2) "value1"

# Another consumer (i.e., 'consumer-2') claims the pending message.
dragonfly$> XCLAIM mystream mygroup consumer-2 10000 "1629392070655-0"
1) 1) "1629392070655-0"
   2) 1) "field1"
      2) "value1"
```

### Using `XCLAIM` with `JUSTID`

Only get the IDs of claimed messages:

```shell
dragonfly$> XCLAIM mystream mygroup consumer-2 10000 "1629392070655-0" JUSTID
1) "1629392070655-0"
```

### Leveraging `IDLE`, `TIME`, and `RETRYCOUNT`

Adjust the message's idle time and retry count upon claiming:

```shell
dragonfly$> XCLAIM mystream mygroup consumer-2 10000 "1629392070655-0" IDLE 5000 RETRYCOUNT 2
1) 1) "1629392070655-0"
   2) 1) "field1"
      2) "value1"
```

## Best Practices

- Use `XCLAIM` in situations where message processing might be taking longer than expected or when a consumer has crashed and you need to reassign messages to other consumers.
- Consider using the `JUSTID` option for better performance if you only need the message IDs.
- Use the `FORCE` option when you want to claim messages that are not assigned to any consumer.
- Always monitor the pending entries list (PEL) to make informed decisions.

## Common Mistakes

- Not providing sufficient `min-idle-time`, which leads to not claiming desired messages as they are not idle long enough.

## FAQs

### What happens if I use `XCLAIM` on messages that are not pending?

Without the `FORCE` option, the command will not successfully claim the messages if they are not in the pending state for the specified consumer group.

### Can `XCLAIM` be used with any stream?

`XCLAIM` can be used with any existing stream where consumer groups have been created and messages are pending.
