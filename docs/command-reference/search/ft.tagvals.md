---
description: Searches the index with a query, returning docs or just IDs
---

# FT.TAGVALS

## Syntax

    FT.TAGVALS index field_name

**Time complexity:** O(N)

**ACL Categories:** @dangerous, @read, @search, @slow

## Description

Return a distinct set of values indexed in a tag field.

## Required arguments

- `index` is the index name. You must first create the index using [`FT.CREATE`](ft.create.md).
- `field_name` is name of a Tag file defined in the schema.

Use `FT.TAGVALS` if your tag indexes things like cities, categories, and so on.

## Limitations

`FT.TAGVALS` provides no paging or sorting, and the tags are not alphabetically sorted.
`FT.TAGVALS` only operates on tag fields. 
The returned strings are lowercase with whitespaces removed, but otherwise unchanged.

## Return

One of the following:

- [Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): an array of distinct tag values as bulk strings.
- [Simple error reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-errors) in these cases: no such index, not a tag field.

## Examples

``` bash
# Create an index on hash keys with 'category' as a tag field.
dragonfly> FT.CREATE idx ON HASH PREFIX 1 blog:post: SCHEMA title TEXT SORTABLE category TAG SORTABLE
OK

# Create a few hash records.
dragonfly> HSET blog:post:1 title "My Blog #1" category engineering
(integer) 2
dragonfly> HSET blog:post:2 title "My Blog #2" category announcement
(integer) 2
dragonfly> HSET blog:post:3 title "My Blog #3" category engineering
(integer) 2

# Get the distinct set of values indexed in the 'category' tag field.
dragonfly> FT.TAGVALS idx category
1) "announcement"
2) "engineering"
```
