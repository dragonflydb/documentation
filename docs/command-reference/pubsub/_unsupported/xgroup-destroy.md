---
description: Learn how to use Redis XGROUP DESTROY to remove a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DESTROY

<PageTitle title="Redis XGROUP DESTROY Explained (Better Than Official Docs)" />

## Syntax

    XGROUP DESTROY key group

**Time complexity:** O(N) where N is the number of entries in the group's pending entries list (PEL).

The `XGROUP DESTROY` command completely destroys a consumer group.

The consumer group will be destroyed even if there are active consumers, and pending messages, so make sure to call this command only when really needed.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of destroyed consumer groups (0 or 1)
