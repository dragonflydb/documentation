---
description: Uses SEARCH command to collect performance info
---

# FT.PROFILE

## Syntax

    FT.PROFILE index SEARCH | AGGREGATE [LIMITED] QUERY query

**Time complexity:** O(N)

## Description

Apply the [`FT.SEARCH`](./ft.search.md) or [`FT.AGGREGATE`](./ft.aggregate.md) command to collect performance details.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name, created using the [`FT.CREATE`](./ft.create.md) command.
</details>

<details open>
<summary><code>SEARCH | AGGREGATE</code></summary>

specifies which command to profile.
- `SEARCH` profiles a search query
- `AGGREGATE` profiles an aggregation query

</details>

<details open>
<summary><code>LIMITED</code></summary>

enables limited profiling mode (planned feature).

:::info Future functionality
The `LIMITED` option is planned for future releases but full functionality is not currently implemented in Dragonfly.
:::
</details>

<details open>
<summary><code>QUERY query</code></summary>

is query string, sent to the [`FT.SEARCH`](./ft.search.md) or [`FT.AGGREGATE`](./ft.aggregate.md) command to collect performance details.
</details>

## Return

`FT.PROFILE` returns an array reply.
The first element of the returned array has the following elements:

- `took`: time in microseconds (μs) used to execute the query.
- `hits`: number of documents returned by the query.
- `serialized`: number of documents serialized by the query.

The rest of the array elements represent an execution tree on every Dragonfly shard with timings.

## Examples

<details open>
<summary><b>Collect performance information about an index</b></summary>

```bash
dragonfly> HSET blog:post:1 title "blog post 1" published_at 1701210030 category "default" description "this is a blog"
(integer) 4

dragonfly> FT.CREATE idx ON HASH PREFIX 1 blog:post: SCHEMA title TEXT SORTABLE published_at NUMERIC SORTABLE category TAG SORTABLE description TEXT NOINDEX
OK

dragonfly> FT.PROFILE idx SEARCH QUERY "@category:{default}"
1) 1) "took"
   2) (integer) 488
   3) "hits"
   4) (integer) 1
   5) "serialized"
   6) (integer) 1
2) 1) "took"
   2) (integer) 13
   3) "tree"
   4) 1) t=9          n=0          Field{category}
      2) 1) t=5          n=0          Tags{default}
3) 1) "took"
   2) (integer) 35
   3) "tree"
   4) 1) t=30         n=0          Field{category}
      2) 1) t=5          n=0          Tags{default}
4) 1) "took"
   2) (integer) 24
   3) "tree"
   4) 1) t=19         n=0          Field{category}
      2) 1) t=14         n=0          Tags{default}
5) 1) "took"
   2) (integer) 54
   3) "tree"
   4) 1) t=11         n=1          Field{category}
      2) 1) t=9          n=1          Tags{default}
6) 1) "took"
   2) (integer) 9
   3) "tree"
   4) 1) t=6          n=0          Field{category}
      2) 1) t=5          n=0          Tags{default}
```
</details>

## See also

[`FT.SEARCH`](./ft.search.md) | [`FT.AGGREGATE`](./ft.aggregate.md)

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
