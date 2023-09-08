---
description: Destroy a consumer group.
---

# XGROUP DESTROY

## Syntax

    XGROUP DESTROY key group

**Time complexity:** O(N) where N is the number of entries in the group's pending entries list (PEL).

The `XGROUP DESTROY` command completely destroys a consumer group.

The consumer group will be destroyed even if there are active consumers, and pending messages, so make sure to call this command only when really needed.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of destroyed consumer groups (0 or 1)