---
description: Delete consumer from a particular group
---

# XGROUP DELCONSUMER

## Syntax

    XGROUP DELCONSUMER key group consumer

**Time complexity:** O(1)

**ACL categories:** @write, @stream, @slow

**XGROUP DELCONSUMER** deletes the specified consumer from
the given consumer **<group\>**. **<key\>** denotes the stream
to which the group belongs. Both stream and group must already
exist.

Note, however, that any pending messages that the consumer had
will become unclaimable after it was deleted. It is strongly
recommended, therefore, that any pending messages are claimed
or acknowledged prior to deleting the consumer from the group.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers):
the number of pending messages that the consumer had before it was
deleted
