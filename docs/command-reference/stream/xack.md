---
description: Acknowledge a received message and removes the message from consumer group's pending entries list.
---

# XACK

## Syntax

    XACK key group id [id ... ]

**Time complexity:** O(1) for each message ID processed.

**ACL categories:** @write, @stream, @fast

**XACK** command acknowledges one or more messages by removing the messages from the pending entries list (PEL) of the specified consumer stream group. A message is pending, and as such stored inside the PEL, when it was delivered to some consumer, normally as a side effect of calling XREADGROUP, or when a consumer took ownership of a message calling XCLAIM. The pending message was delivered to some consumer but the server is yet not sure it was processed at least once. So new calls to XREADGROUP to grab the messages history for a consumer (for instance using an ID of 0), will return such message. Similarly the pending message will be listed by the XPENDING command, that inspects the PEL. Once a consumer successfully processes a message, it should call **XACK** so that such message does not get processed again, and as a side effect, the PEL entry about this message is also purged, releasing memory from the Dragonfly server.


## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

The command returns the number of messages successfully acknowledged. Certain message IDs may no longer be part of the PEL (for example because they have already been acknowledged), and XACK will not count them as successfully acknowledged.

## Examples

```shell
dragonfly> XACK mystream mygroup 1526569495631-0
(integer) 1
```
