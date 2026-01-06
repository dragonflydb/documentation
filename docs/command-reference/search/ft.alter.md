---
description: Searches the index with a query, returning docs or just IDs
---

# FT.ALTER

## Syntax

```
FT.ALTER {index} [SKIPINITIALSCAN] SCHEMA ADD {attribute} {options} ...
```

**Time complexity:** O(N) where N is the number of keys in the keyspace

**ACL Categories:** @search

## Description

Add a new attribute to the index.
Note that adding an attribute to the index causes any future document updates to use the new attribute when indexing and reindexing existing documents.

## Required arguments

- The `index` parameter is the index name to alter.
- The `SKIPINITIALSCAN` option: if set, the command does not scan and index.
- After the `SCHEMA ADD` keywords, declares which fields to add:
  - `attribute` is an attribute to add.
  - `options` are attribute options. Refer to [`FT.CREATE`](ft.create.md) for more information.

## Return Values

- [Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` if executed correctly.
- [Simple error reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-errors) in these cases: no such index, invalid schema syntax.

## Examples

``` bash
dragonfly> FT.ALTER idx SCHEMA ADD id2 NUMERIC SORTABLE
OK
```
