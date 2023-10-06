---
description: Read entries from a stream for a consumer group
---

# XREADGROUP

## Syntax

	XREADGROUP GROUP group consumer [COUNT count] [BLOCK milliseconds]
      [NOACK] STREAMS key [key ...] id [id ...]

**Time Complexity:** For each stream mentioned: O(M) with M being the number of elements returned.
If M is constant (e.g. always asking for the first 10 elements with COUNT), you can consider it O(1).
On the other side when `XREADGROUP` blocks, [`XADD`](./xadd.md) will pay the O(N) time in order to serve the N clients blocked on the stream getting new data.

**ACL categories:** @write, @stream, @slow, @blocking

The `XREADGROUP` command is a special version of the [`XREAD`](./xread.md) command with support for consumer groups.
It is recommended to understand the [`XREAD`](./xread.md) command before reading this page.

You can learn more about Streams [here](https://redis.io/docs/data-types/streams/).

## Differences Between `XREAD` & `XREADGROUP`

From the point of view of the syntax, the commands are almost the same, however `XREADGROUP` requires a special and mandatory option:

```text
GROUP <group-name> <consumer-name>
```

The `group-name` argument is the name of a consumer group associated to the stream.
The group is created using the [`XGROUP CREATE`](./xgroup-create.md) command.
The consumer name is the string that is used by the client to identify itself inside the group.
The consumer is auto created inside the consumer group the first time it is seen.
Different clients should select a different consumer name.

When you read with `XREADGROUP`, the server will remember that a given message was delivered to you:
the message will be stored inside the consumer group in what is called a **Pending Entries List (PEL)**,
that is a list of message IDs delivered but not yet acknowledged.

The client will have to acknowledge the message processing using [`XACK`](./xack.md) in order for the pending entry to be removed from the PEL.
The PEL can be inspected using the [`XPENDING`](./xpending.md) command.

The `NOACK` subcommand can be used to avoid adding the message to the PEL in cases where reliability is not a requirement and the occasional message loss is acceptable.
This is equivalent to acknowledging the message when it is read.

The ID(s) to specify in the `STREAMS` option when using `XREADGROUP` can be one of the following two:

- The special `>` ID, which means that the consumer want to receive only messages that were never delivered to any other consumer.
  It just means, give me new messages. 
- Any other ID, that is, `0` or any other valid ID or incomplete ID (just the millisecond time part),
  will have the effect of returning entries that are pending for the consumer sending the command with IDs greater than the one provided.
  So basically if the ID is not `>`, then the command will just let the client access its pending entries: messages delivered to it, but not yet acknowledged.
  Note that in this case, both `BLOCK` and `NOACK` options are ignored.

Like [`XREAD`](./xread.md), the `XREADGROUP` command can be used in a blocking way.
There are no differences in this regard.

## Message Delivery

When a message is delivered to a consumer (i.e., read by using `XREADGROUP`), two things happen:

1. If the message was never delivered to anyone (i.e., a new message) then a PEL (Pending Entries List) is created.
2. If instead the message was already delivered to this consumer, and it is just re-fetching the same message again,
   then the last delivery counter is updated to the current time, and the number of deliveries is incremented by one.
   You can access those message properties using the [`XPENDING`](./xpending.md) command.

## Message Deletion

Entries may be deleted from the stream due to trimming or explicit [`XDEL`](./xdel.md) at any time.
Dragonfly doesn't prevent the deletion of entries that are present in the stream's PELs.
When this happens, the PELs retain the deleted entries' IDs, but the actual entry payload is no longer available.
Therefore, when reading such PEL entries, Dragonfly will return a null value in place of their respective data.
See the [Read Deleted Messages](#read-deleted-messages) section below for more information.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays), specifically:

The command returns an array of results: each element of the returned array is an array composed of a two element containing the key name and the entries reported for that key.
The entries reported are full stream entries, having IDs and the list of all the fields and values.
Field and values are guaranteed to be reported in the same order they were added by [`XADD`](./xadd.md).

When `BLOCK` is used, a `null` reply is returned upon timeout.

## Examples

### Basic Usage

Normally you can use the `XREADGROUP` command to get new messages and process them. In pseudocode:

```shell
WHILE true
    entries = XREADGROUP GROUP $GroupName $ConsumerName BLOCK 2000 COUNT 10 STREAMS mystream >
    if entries == nil
        puts "Timeout... try again"
        CONTINUE
    end

    FOREACH entries AS stream_entries
        FOREACH stream_entries as message
            process_message(message.id,message.fields)

            # ACK the message as processed
            XACK mystream $GroupName message.id
        END
    END
END
```

In this way the example consumer code will fetch only new messages, process them, and acknowledge them via [`XACK`](./xack.md).
However, the pseudocode above does not handle recovering after a crash.
If the consumer code crashes in the middle of processing messages, messages will remain in the PEL.
We can access historical messages by giving `XREADGROUP` initially an ID of `0`, and performing the same loop.
Once providing an ID of `0` the reply is an empty set of messages, we know that we processed and acknowledged all the pending messages.
From there, we can start to use `>` as ID, in order to get the new messages and rejoin the consumers that are processing new messages.

### Read Deleted Messages

As mentioned earlier, when a message is deleted from a stream, it is not removed from the consumer group's PEL.
When reading such PEL entries, Dragonfly will return a null value in place of their respective data.

```shell
dragonfly> XADD mystream 1 myfield mydata
"1-0"

dragonfly> XGROUP CREATE mystream mygroup 0
OK

dragonfly> XREADGROUP GROUP mygroup myconsumer STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1-0"
         2) 1) "myfield"
            2) "mydata"

dragonfly> XDEL mystream 1-0
(integer) 1

dragonfly> XREADGROUP GROUP mygroup myconsumer STREAMS mystream 0
1) 1) "mystream"
   2) 1) 1) "1-0"
         2) (nil)
```
