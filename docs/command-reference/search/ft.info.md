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
- `index_definition`: contains information about the index configuration, including `key_type` and `prefix`.
- `attributes`: index schema - for each field contains:
  - `identifier`: the original field name or JSONPath 
  - `attribute`: the field alias (or same as identifier if no alias provided)
  - `type`: field type (TEXT, TAG, NUMERIC, VECTOR, GEO)
  - field-specific options like `SORTABLE` and `NOINDEX` flags when applicable
- `num_docs`: Number of documents in the index.

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
3) index_definition
4) 1) key_type
   2) HASH
   3) prefix
   4) blog:post:
5) attributes
6) 1) 1) identifier
      2) description
      3) attribute
      4) description
      5) type
      6) TEXT
      7) NOINDEX
   2) 1) identifier
      2) published_at
      3) attribute
      4) published_at
      5) type
      6) NUMERIC
      7) SORTABLE
      8) blocksize
      9) 7000
   3) 1) identifier
      2) title
      3) attribute
      4) title
      5) type
      6) TEXT
      7) SORTABLE
   4) 1) identifier
      2) category
      3) attribute
      4) category
      5) type
      6) TAG
      7) SORTABLE
7) num_docs
8) (integer) 1
```
</details>

## See also

[`FT.CREATE`](./ft.create.md) | [`FT.SEARCH`](./ft.search.md)

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
