---
description:  Learn how to use the Redis MEMORY USAGE command to report the memory a key consumes in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY USAGE

<PageTitle title="Redis MEMORY USAGE Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY USAGE key [WITHOUTKEY]

**Time complexity:** O(1) for strings, O(N) for collection types where N is the number of elements.

**ACL categories:** @read, @slow

The `MEMORY USAGE` command reports the number of bytes that the value stored at `key` requires,
including the memory needed to store the key itself.

If the `WITHOUTKEY` option is given, only the value is accounted for. `WITHOUTKEY` is
Dragonfly-specific.

Dragonfly stores values that are small enough directly inside the key table rather than in a
separate allocation. Such values have no allocation of their own, so `MEMORY USAGE` reports `0`
for them.

The `SAMPLES` option that Redis accepts is not supported. Extra arguments after the key are
ignored rather than rejected, so `MEMORY USAGE key SAMPLES 0` behaves the same as
`MEMORY USAGE key`.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the number of bytes used by the key
and its value.

[Null reply](https://valkey.io/topics/protocol/#nulls): if `key` does not exist.

## Examples

A small string is stored inline and reports no allocation of its own, while a larger one does:

```shell
dragonfly> SET tiny abc
OK
dragonfly> MEMORY USAGE tiny
(integer) 0

dragonfly> STRLEN bigstr
(integer) 2000
dragonfly> MEMORY USAGE bigstr
(integer) 1792
```

Collections account for their elements:

```shell
dragonfly> LLEN biglist
(integer) 200
dragonfly> MEMORY USAGE biglist
(integer) 3672
```

`WITHOUTKEY` excludes the key itself, which is noticeable with long key names:

```shell
dragonfly> MEMORY USAGE kkkkkkkk...kkk
(integer) 3264
dragonfly> MEMORY USAGE kkkkkkkk...kkk WITHOUTKEY
(integer) 3072
```

A key that does not exist reports nothing:

```shell
dragonfly> MEMORY USAGE nosuchkey
(nil)
```

## See also

[`MEMORY`](./memory.md) | [`MEMORY STATS`](./memory-stats.md) | [`INFO`](./info.md)
