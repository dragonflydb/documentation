---
description:  Learn how to use Redis XPENDING to list pending messages of a stream's consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XPENDING

<PageTitle title="Redis XPENDING Command (Documentation) | Dragonfly" />

## Syntax

	XPENDING key group [[IDLE min-idle-time] start end count [consumer]]

**Time Complexity:** O(N) with N being the number of elements returned, so asking for a small fixed number of entries per call is O(1).
O(M), where M is the total number of entries scanned when used with the IDLE filter.
When the command returns just the summary and the list of consumers is small, it runs in O(1) time; otherwise, an additional O(N) time for iterating every consumer.

**ACL categories:** @read, @stream, @slow

Fetching data from a stream via a consumer group, and not acknowledging such data, has the effect of creating pending entries.
This is well explained in the `XREADGROUP` command.
You can also learn more about Streams [here](https://redis.io/docs/data-types/streams/).

The `XACK` command will immediately remove the pending entry from the Pending Entries List (PEL) since once a message is successfully processed,
there is no longer need for the consumer group to track it and to remember the current owner of the message.

The `XPENDING` command is the interface to inspect the list of pending messages,
and is as thus a very important command in order to observe and understand what is happening with a streams consumer groups:
what clients are active, what messages are pending to be consumed, or to see if there are idle messages.
Moreover, this command, together with [`XCLAIM`](./xclaim.md) is used in order to implement recovering of consumers that are failing for a long time,
and as a result certain messages are not processed: a different consumer can claim the message and continue.

## Summary Form

When `XPENDING` is called with just a key name and a consumer group name, it just returns output in the **summary form** about the pending messages in a given consumer group.
In the following example, we create a consumer group and immediately create a pending message by reading from the group with `XREADGROUP`.

```shell
dragonfly> XADD mystream * name Alice surname Adams
"1695755830453-0"

dragonfly> XADD mystream * name John surname Doe
"1695755847112-0"

dragonfly> XGROUP CREATE mystream mygroup 0-0
OK

dragonfly> XREADGROUP GROUP mygroup consumer-123 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1695755830453-0"
         2) 1) "name"
            2) "Alice"
            3) "surname"
            4) "Adams"
```

We expect the pending entries list for the consumer group `mygroup` to have a message right now: consumer named `consumer-123` fetched the message without acknowledging its processing.
The simple summary form of `XPENDING` will give us this information:

```shell
dragonfly> XPENDING mystream mygroup
1) (integer) 1
2) "1695755830453-0"
3) "1695755830453-0"
4) 1) 1) "consumer-123"
      2) (integer) 1
```

In this form, the command outputs the total number of pending messages for this consumer group, which is one, followed by the smallest and greatest ID among the pending messages,
and then list every consumer in the consumer group with at least one pending message, and the number of pending messages it has.

## Extended Form

The summary form provides a good overview, but sometimes we are interested in the details.
In order to see all the pending messages, in the **extended form**, with more associated information we need to also pass a range of IDs, in a similar way we do it with [`XRANGE`](./xrange.md) ,
and a non-optional count argument, to limit the number of messages returned per call:

```shell
dragonfly> XPENDING mystream mygroup - + 10
1) 1) "1695755830453-0"
   2) "consumer-123"
   3) (integer) 1257837
   4) (integer) 1
```

In the extended form we no longer see the summary information, instead there is detailed information for each message in the pending entries list.
For each message four attributes are returned:

1. The ID of the message.
2. The current owner of the message (i.e., the consumer that fetched the message and has still to acknowledge it).
3. The number of milliseconds that elapsed since the last time this message was delivered to this consumer. 
4. The number of times this message was delivered.

The deliveries counter, that is the fourth element in the array, is incremented when some other consumer claims the message with [`XCLAIM`](./xclaim.md)
or when the message is delivered again via `XREADGROUP`, when accessing the history of a consumer in a consumer group.

It is possible to pass an additional argument to the command, in order to see the messages having a specific owner:

```shell
dragonfly> XPENDING mystream mygroup - + 10 consumer-123
```

But in the above case the output would be the same, since we have pending messages only for a single consumer `consumer-123`.
However, what is important to keep in mind is that this operation, filtering by a specific consumer, is not inefficient even when there are many pending messages from many consumers:
we have a pending entries list data structure both globally, and for every consumer, so we can very efficiently show just messages pending for a single consumer.

## Idle Time Filter

It is also possible to filter pending stream entries by their idle-time, given in milliseconds (useful for [`XCLAIM`](./xclaim.md)ing entries that have not been processed for some time):

```shell
dragonfly> XPENDING mystream mygroup IDLE 9000 - + 10
dragonfly> XPENDING mystream mygroup IDLE 9000 - + 10 consumer-123
```

The first case will return the first 10 (or less) PEL entries of the entire group that are idle for over 9 seconds, whereas in the second case only those of `consumer-123`.

## Pending Entries List & Exclusive Ranges

The `XPENDING` command allows iterating over the Pending Entries List (PEL) just like [`XRANGE`](./xrange.md) and [`XREVRANGE`](./xrevrange.md) allow for the stream's entries.
You can do this by prefixing the ID of the last-read pending entry with the `(` character that denotes an open (exclusive) range, and proving it to the subsequent call to the command.

By default, the command returns entries including specified IDs:

```shell
dragonfly> XPENDING mystream mygroup 1695755830453-0 + 10
1) 1) "1695755830453-0"
   2) "consumer-123"
   3) (integer) 1577015
   4) (integer) 1
```

If the ID is prefixed with `(`, the range is exclusive:

```shell
dragonfly> XPENDING mystream mygroup (1695755830453-0 + 10
(empty array)
```

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays), specifically:

- The command returns data in different format depending on the way it is called, as previously explained in this page.
- However, the reply is always an array of items.
