---
description: Learn how to use Dragonfly's MEMORY DECOMMIT command to return freed memory to the operating system.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY DECOMMIT

<PageTitle title="Dragonfly MEMORY DECOMMIT Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY DECOMMIT [COOL]

**Time complexity:** Depends on the amount of memory to decommit.

**ACL categories:** @read, @slow

`MEMORY DECOMMIT` asks Dragonfly's allocator to return memory that the server
has already freed back to the operating system.

With the `COOL` option, Dragonfly instead flushes the tiered-storage cool queue
to disk. This option is useful only when tiered storage is configured.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`.

## Examples

```shell
dragonfly> MEMORY DECOMMIT
OK
```
