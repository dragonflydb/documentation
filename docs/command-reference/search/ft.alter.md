---
description: Searches the index with a query, returning docs or just IDs
---

# FT.SEARCH

## Syntax

    FT.ALTER {index} [SKIPINITIALSCAN] SCHEMA ADD {attribute} {options} ...

**Time complexity:** O(N)
**ACL Categories:** @search

## Description

Add a new attribute to the index. Adding an attribute to the index causes any future document updates to use the new attribute when indexing and reindexing existing documents.

## Required arguments

<details open>
<summary><code>index</code></summary>
is index name to create.

<details open>
<summary><code>SKIPINITIALSCAN</code></summary>
if set, does not scan and index.

<details open>
<summary><code> SCHEMA ADD {attribute} {options} ... </code></summary>

after the SCHEMA keyword, declares which fields to add:

attribute is attribute to add.
options are attribute options. Refer to FT.CREATE for more information.

## Return Values

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` on success.

[Simple error reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-errors):
no such index, invalid schema syntax.

## Examples

``` bash
dragonfly> FT.ALTER idx SCHEMA ADD id2 NUMERIC SORTABLE
OK
```
