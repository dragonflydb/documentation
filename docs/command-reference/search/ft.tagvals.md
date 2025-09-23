---
description: Searches the index with a query, returning docs or just IDs
---

# FT.TAGVALS

## Syntax

FT.TAGVALS index field_name

**Time complexity:** O(N)
**ACL Categories:** @dangerous, @read, @search, @slow

## Description

Return a distinct set of values indexed in a Tag field

## Required arguments

<details open>
<summary><code>index</code></summary>

is full-text index name. You must first create the index using FT.CREATE.

<details open>
<summary><code>field_name</code></summary>

is name of a Tag file defined in the schema.

Use FT.TAGVALS if your tag indexes things like cities, categories, and so on.

## Limitations

FT.TAGVALS provides no paging or sorting, and the tags are not alphabetically sorted. FT.TAGVALS only operates on tag fields. 
The returned strings are lowercase with whitespaces removed, but otherwise unchanged.

## Return

One of the following:

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays):
Array of distinct tag values as bulk strings.

[Simple error reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-errors):
no such index, not a tag field.

## Examples


``` bash
dragonfly> FT.TAGVALS idx tag
"hi from dragonfly"
```
