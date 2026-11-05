---
description: Learn how to use FT.ALIASDEL to remove a Dragonfly search index alias without deleting its index.
---

import PageTitle from '@site/src/components/PageTitle';

# FT.ALIASDEL

<PageTitle title="FT.ALIASDEL Command (Documentation) | Dragonfly" />

## Syntax

    FT.ALIASDEL alias

**Time complexity:** O(1) on average per shard.

**ACL categories:** @ft_search, @slow, @write

Removes an existing search index alias. The target index and its documents
remain intact and can still be accessed using the index name or other aliases.

## Arguments and behavior

`alias` must name an existing alias. Passing an index name does not delete the
index and returns an error if there is no alias with that name.

After deletion, queries using that alias fail unless the name is created again.
Use [`FT.DROPINDEX`](./ft.dropindex.md) to remove the index itself. Dropping an
index also removes the aliases that refer to it.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`
when the alias is removed.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if the alias
does not exist. Deleting the same alias a second time returns an error.

## Examples

Create an index with an alias, remove the alias, and query the underlying index directly:

```shell
dragonfly> FT.CREATE products-v2 ON HASH PREFIX 1 v2: SCHEMA title TEXT
OK

dragonfly> HSET v2:1 title second
(integer) 1

dragonfly> FT.ALIASADD products products-v2
OK

dragonfly> FT.ALIASDEL products
OK

dragonfly> FT.SEARCH products * NOCONTENT
(error) ERR products: no such index

dragonfly> FT.SEARCH products-v2 * NOCONTENT
1) (integer) 1
2) "v2:1"

dragonfly> FT.ALIASDEL products
(error) ERR Alias does not exist
```

## See also

[`FT.ALIASADD`](./ft.aliasadd.md) | [`FT.ALIASUPDATE`](./ft.aliasupdate.md) | [`FT.DROPINDEX`](./ft.dropindex.md) | [`FT.SEARCH`](./ft.search.md)
