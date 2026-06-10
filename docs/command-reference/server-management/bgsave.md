---
description:  Learn how to use Redis BGSAVE command to create a backup of the database in background.
---

import PageTitle from '@site/src/components/PageTitle';

# BGSAVE

<PageTitle title="Redis BGSAVE Command (Documentation) | Dragonfly" />

## Syntax

    BGSAVE [SCHEDULE] [RDB|DF] [cloud_uri] [filename]

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

Equivalent to [SAVE](../server-management/save) and kept for compatibility reasons.

The optional `SCHEDULE` subcommand is accepted for client compatibility but is a no-op: concurrent saves are still rejected and saves are not queued.

[tp]: https://redis.io/topics/persistence

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`. Dragonfly replies with a plain `OK` for `BGSAVE` (including when invoked with the `SCHEDULE` subcommand), not the Redis-style `Background saving started` / `Background saving scheduled` strings.
