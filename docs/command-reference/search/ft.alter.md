---
description: Searches the index with a query, returning docs or just IDs
---

# FT.ALTER

## Syntax

```
FT.ALTER {index} SCHEMA ADD {attribute} {options} ...
```

**Time complexity:** O(N) where N is the number of keys in the keyspace

**ACL Categories:** @ft_search, @slow, @write

## Description

Add a new attribute to the index.
The index can be referenced by its name or by an alias.
Adding an attribute rebuilds the index: existing documents are reindexed with the new attribute, and later document updates use it too.

## Required arguments

- The `index` parameter is the index name or alias to alter.
- After the `SCHEMA ADD` keywords, declares which fields to add:
  - `attribute` is an attribute to add.
  - `options` are attribute options. Refer to [`FT.CREATE`](ft.create.md) for more information.

## Return Values

- [Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if executed correctly.
- [Simple error reply](https://valkey.io/topics/protocol/#simple-errors) in these cases: no such index, invalid schema syntax.

## Examples

``` bash
dragonfly> FT.CREATE idx ON HASH SCHEMA id NUMERIC
OK
dragonfly> FT.ALTER idx SCHEMA ADD id2 NUMERIC SORTABLE
OK
```
