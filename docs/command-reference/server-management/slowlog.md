---
description:  Learn how to use Redis SLOWLOG command to manage the Redis server slowlog.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG

<PageTitle title="Redis SLOWLOG Command (Documentation) | Dragonfly" />

## Syntax

    SLOWLOG [GET | LEN | RESET | HELP]

**ACL categories:** @slow, @admin

This is a container command for slowlog management commands.

<!-- To see the list of available commands you can call `SLOWLOG HELP`. -->