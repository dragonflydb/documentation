---
description: Returns information and statistics on the index
---

# FT.INFO

## Syntax

    FT.INFO index

**Time complexity:** O(1)

## Description

Return information and statistics on the index.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using [`FT.CREATE`](./ft.create.md).
</details>

## Return

`FT.INFO` returns an array reply with pairs of keys and values.

Returned values include:

- `index_name`: name of the index upon creation by using [`FT.CREATE`](./ft.create.md).
- `fields`: index schema - field names, types, and attributes.
- `num_docs`: Number of documents.

## Examples

<details open>
<summary><b>Return statistics about an index</b></summary>

```bash
dragonfly> HSET blog:post:1 title "blog post 1" published_at 1701210030 category "default" description "this is a blog"
(integer) 4

dragonfly> FT.CREATE idx ON HASH PREFIX 1 blog:post: SCHEMA title TEXT SORTABLE published_at NUMERIC SORTABLE category TAG SORTABLE description TEXT NOINDEX
OK

dragonfly> FT.INFO idx
1) index_name
2) idx
3) fields
4) 1) 1) identifier
      2) published_at
      3) attribute
      4) published_at
      5) type
      6) NUMERIC
   2) 1) identifier
      2) title
      3) attribute
      4) title
      5) type
      6) TEXT
   3) 1) identifier
      2) category
      3) attribute
      4) category
      5) type
      6) TAG
   4) 1) identifier
      2) description
      3) attribute
      4) description
      5) type
      6) TEXT
5) num_docs
6) (integer) 1
```
</details>

## See also

[`FT.CREATE`](./ft.create.md) | [`FT.SEARCH`](./ft.search.md)
