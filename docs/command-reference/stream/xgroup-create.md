---
description: Create consumer group
---

# XGROUP CREATE

## Syntax

    XGROUP CREATE key group <id | $> [MKSTREAM]

**Time complexity:** O(1)

**ACL categories:** @write, @stream, @slow

Create a new consumer group for the specified stream. *group* is
the name of the consumer group. *key* is the stream name.

A consumer group is a collection of consumers. Group is extreamly
useful when it is required to distribute incoming stream entries
to different consumers. Each group has its own *pending entry list*
(PEL) where it stores the group received entries. Consumers only
recieves entries that no other consumers already received from the
group.

If a group already exists by the given name, **XGROUP** throws a
**-BUSYGROUP** error.

The **XGROUP** command requires an **<id\>** argument. It tells the
command to set the last delivered entry of the newly created group
to the specified ID. Entries with lower IDs than the last delivered
entry do not belong to the group and hence consumers can't receive
those entries.

If you want to set the last delivered entry to the latest stream
entry and you don't want to mention the ID explicitly, you can use
the special "**$**" character. When specified, it sets the last
delivery entry to the latest entry.

By default, the **XGROUP CREATE** command expects that the target stream
exists, and returns an error when it doesn't. If a stream does not exist,
you can create it automatically with length of 0 by using the
optional **MKSTREAM** subcommand as the last argument after the **<id\>**:

```shell
XGROUP CREATE mystream mygroup $ MKSTREAM
```

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings):
**OK** on success.
