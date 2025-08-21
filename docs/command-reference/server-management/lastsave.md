---
description:  Learn how to use Redis LASTSAVE command to obtain the UNIX timestamp of the last database save.
---

import PageTitle from '@site/src/components/PageTitle';

# LASTSAVE

<PageTitle title="Redis LASTSAVE Command (Documentation) | Dragonfly" />

## Syntax

    LASTSAVE 

**Time complexity:** O(1)

**ACL categories:** @admin, @fast, @dangerous

Return the UNIX TIME of the last DB save executed with success.
A client may check if a `BGSAVE` command succeeded reading the `LASTSAVE` value,
then issuing a `BGSAVE` command and checking at regular intervals every N
seconds if `LASTSAVE` changed. Dragonfly considers the database saved successfully at startup.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): an UNIX time stamp.
