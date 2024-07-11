---
description:  Learn how to use Redis XGROUP SETID to set the last delivered ID of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP SETID

<PageTitle title="Redis XGROUP SETID Command (Documentation) | Dragonfly" />

## Syntax

    XGROUP SETID key group <id | $>

**Time complexity:** O(1)

**ACL categories:** @write, @stream, @slow

Set the last delivered ID of a consumer group.

Normally, a consumer group's last delivered ID is set when the
group is created with **XGROUP CREATE**. The **XGROUP SETID**
command allows modifying the group's last delivered ID, without
having to delete and recreate the group. For instance if you want
the consumers in a consumer group to re-process all the messages
in a stream, you may want to set its next ID to 0:

```shell
XGROUP SETID mystream mygroup 0
```

## Return
[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings):
OK on success.
