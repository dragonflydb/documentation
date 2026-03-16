---
description:  Learn how to use Redis ECHO command to display provided string.
---

import PageTitle from '@site/src/components/PageTitle';

# ECHO

<PageTitle title="Redis ECHO Command (Documentation) | Dragonfly" />

## Syntax

    ECHO message

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

Returns `message`.

## Return

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings)

## Examples

```shell
dragonfly> ECHO "Hello World!"
"Hello World!"
```
