---
description:  Learn how to use Redis BGSAVE command to create a backup of the database in background.
---

import PageTitle from '@site/src/components/PageTitle';

# BGSAVE

<PageTitle title="Redis BGSAVE Command (Documentation) | Dragonfly" />

## Syntax

    BGSAVE SAVE [RDB|DF] [cloud_uri] [filename]

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

Equvalent to [SAVE](../server-management/save) and kept for compatibility reasons.


[tp]: https://redis.io/topics/persistence

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `Background saving started` if `BGSAVE` started correctly or `Background saving scheduled` when used with the `SCHEDULE` subcommand.
