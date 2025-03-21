---
description:  Learn how to use Redis CLIENT unpause command to unblock paused clients.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT UNPAUSE

<PageTitle title="Redis CLIENT UNPAUSE (Documentation) | Dragonfly" />

## Syntax

    CLIENT UNPAUSE

**Time complexity:** O(N) Where N is the number of paused clients
**ACL categories:** @admin, @slow, @dangerous, @connection

CLIENT UNPAUSE is used to resume command processing for all clients that were paused by CLIENT PAUSE.

## Return
Simple string reply: OK.
