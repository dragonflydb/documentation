---
description: Learn how to use Redis MEMORY USAGE command to measure a key's memory use in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY USAGE

<PageTitle title="Redis MEMORY USAGE Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY USAGE key [WITHOUTKEY]

**Time complexity:** O(1)

**ACL categories:** @read, @slow

`MEMORY USAGE` returns the number of bytes used by a key and its value. By
default, the key's own memory is included. Use `WITHOUTKEY` to return only the
memory used by the value.

Dragonfly does not support Redis/Valkey's `SAMPLES` option.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the number of
bytes used by the key, or a [null reply](https://valkey.io/topics/protocol/#nulls)
when the key does not exist.

## Examples

```shell
dragonfly> MEMORY USAGE greeting
dragonfly> MEMORY USAGE greeting WITHOUTKEY
```
