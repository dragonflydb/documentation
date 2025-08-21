---
description:  Discover how to use Redis SLOWLOG RESET command to clear all the entries from the slow log.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG RESET

<PageTitle title="Redis SLOWLOG RESET Command (Documentation) | Dragonfly" />

## Syntax

    SLOWLOG RESET

This command resets the slow log, clearing all entries in it.
Once deleted the information is lost forever.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK`
