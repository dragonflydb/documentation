---
description: Learn how to use FT.ALIASUPDATE to create or redirect a Dragonfly search index alias.
---

import PageTitle from '@site/src/components/PageTitle';

# FT.ALIASUPDATE

<PageTitle title="Redis FT.ALIASUPDATE Command (Documentation) | Dragonfly" />

## Syntax

    FT.ALIASUPDATE alias index

**Time complexity:** O(1) on average per shard.

**ACL categories:** @ft_search

Changes an alias to refer to the specified search index. **If the alias does
not exist, this command creates it.** Use [`FT.ALIASADD`](./ft.aliasadd.md)
when an existing alias should cause an error.

:::note Availability

Verified with the Dragonfly development build `df-2cd7a2e`. This command is not
available in Dragonfly v2.0.2.

:::

## Arguments and behavior

- `alias`: the alias to create or update. Its name must not conflict with an
  existing index.
- `index`: an existing index name. Another alias cannot be used as the target.

Updating the alias changes which index subsequent queries through that alias
use. It does not rebuild, copy, or delete either index or their documents.
Prepare the replacement index before switching the alias to it.

If the requested target is missing or is an alias, the command returns an error
and leaves the existing mapping unchanged.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`
when the alias is created or updated.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if the alias
name conflicts with an index, or the target is missing or is itself an alias.

## Examples

Starting with the `products` alias and `products-v1` index from the
[`FT.ALIASADD` example](./ft.aliasadd.md#examples), create a replacement index
and switch the alias:

```shell
dragonfly> FT.CREATE products-v2 ON HASH PREFIX 1 v2: SCHEMA title TEXT
OK

dragonfly> HSET v2:1 title second
(integer) 1

dragonfly> FT.ALIASUPDATE products products-v2
OK

dragonfly> FT.SEARCH products * NOCONTENT
1) (integer) 1
2) "v2:1"

dragonfly> FT.ALIASUPDATE products missing
(error) ERR Unknown index name or name is alias

dragonfly> FT.SEARCH products * NOCONTENT
1) (integer) 1
2) "v2:1"
```

An alias that does not exist is created:

```shell
dragonfly> FT.ALIASUPDATE new-alias products-v1
OK
```

## See also

[`FT.ALIASADD`](./ft.aliasadd.md) | [`FT.ALIASDEL`](./ft.aliasdel.md) | [`FT.CREATE`](./ft.create.md) | [`FT.SEARCH`](./ft.search.md)
