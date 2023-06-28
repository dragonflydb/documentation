---
description: Delete entries from stream
---

# XDEL

## Syntax

    XDEL key id [id ...]

**Time complexity:** O(1) for each single item to delete in the stream.

**XDEL** deletes entries from the given stream. The key and ids specify
the stream name and entry IDs respectively. Refer to [XADD referece
page](./xadd.md#specifying-id) for more information about IDs.

## Return

[Integer Reply](https://redis.io/docs/reference/protocol-spec#resp-integers).
**XDEL** returns the number of deleted entries.

## Example

```shell
dragonfly> XADD mystream * name John
"1623910120014-0"
dragonfly> XADD mystream * name Bob
"1623910467320-0"
dragonfly> XDEL mystream 1623910120014-0 1-1
(integer) 1
```
