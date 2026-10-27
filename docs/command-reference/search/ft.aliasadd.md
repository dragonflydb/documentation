---
description: Learn how to use FT.ALIASADD to give a Dragonfly search index an alternate name.
---

import PageTitle from '@site/src/components/PageTitle';

# FT.ALIASADD

<PageTitle title="Redis FT.ALIASADD Command (Documentation) | Dragonfly" />

## Syntax

    FT.ALIASADD alias index

**Time complexity:** O(1) on average per shard.

**ACL categories:** @ft_search

Adds an alternate name for an existing search index. Applications can query
the alias with [`FT.SEARCH`](./ft.search.md) and later switch it to another
index with [`FT.ALIASUPDATE`](./ft.aliasupdate.md), keeping the same name in
their queries.

:::note Availability

Verified with the Dragonfly development build `df-2cd7a2e`. This command is not
available in Dragonfly v2.0.2.

:::

## Arguments and behavior

- `alias`: a new alias name. It must not already name an alias or an index.
- `index`: an existing index created with [`FT.CREATE`](./ft.create.md).
  The target must be an index name, not another alias.

An alias refers to an index without copying its data or creating a new index.
Multiple aliases can refer to the same index. [`FT._LIST`](./ft._list.md)
lists index names, not aliases. Dropping the target index removes its aliases.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`
when the alias is created.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if the alias
already exists, its name conflicts with an index, or the target is missing or
is itself an alias. Adding an existing alias fails even if it already points
to the requested index.

## Examples

Create an index and query it through an alias:

```shell
dragonfly> FT.CREATE products-v1 ON HASH PREFIX 1 v1: SCHEMA title TEXT
OK

dragonfly> HSET v1:1 title first
(integer) 1

dragonfly> FT.ALIASADD products products-v1
OK

dragonfly> FT.SEARCH products * NOCONTENT
1) (integer) 1
2) "v1:1"

dragonfly> FT.ALIASADD products products-v1
(error) ERR Alias already exists
```

## See also

[`FT.ALIASUPDATE`](./ft.aliasupdate.md) | [`FT.ALIASDEL`](./ft.aliasdel.md) | [`FT.CREATE`](./ft.create.md) | [`FT.SEARCH`](./ft.search.md)
