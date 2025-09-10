---
description:  Learn how to use Redis CLIENT command to manage clients connected to the Redis server.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT

<PageTitle title="Redis CLIENT Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT 

**Time complexity:** Depends on subcommand.

This is a container command for client connection commands.

Currently, the following subcommands are supported:

- [CLIENT CACHING](./client-caching.md)
- [CLIENT GETNAME](./client-getname.md)
- [CLIENT ID](./client-id.md)
- [CLIENT KILL](./client-kill.md)
- [CLIENT LIST](./client-list.md)
- [CLIENT UNPAUSE](./client-unpause.md)
- [CLIENT PAUSE](./client-pause.md)
- [CLIENT SETNAME](./client-setname.md)
- [CLIENT SETINFO](./client-setinfo.md)
- [CLIENT TRACKING](./client-tracking.md)
- CLIENT MIGRATE
- [CLIENT HELP](./client-help.md)

<!-- To see the list of available commands you can call `CLIENT HELP`. -->