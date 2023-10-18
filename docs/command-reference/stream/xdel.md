---
description:  Learn how to use Redis XDEL to delete a message from a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XDEL

<PageTitle title="Redis XDEL Command (Documentation) | Dragonfly" />

## Syntax

    XDEL key id [id ...]

**Time complexity:** O(1) for each single item to delete in the stream.

**ACL categories:** @write, @stream, @fast

**XDEL** deletes entries from the given stream. The key and ids specify
the stream name and entry IDs respectively. Refer to [XADD referece
page](./xadd.md#specifying-id) for more information about IDs.

## Return

[Integer Reply](https://redis.io/docs/reference/protocol-spec/#integers).
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
