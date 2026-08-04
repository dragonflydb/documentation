---
description: Runs a search query and performs aggregate transformations
---

# FT.AGGREGATE

## Syntax

    FT.AGGREGATE index query
      [LOAD count field [field ...]]
      [GROUPBY nargs property [property ...] [REDUCE function nargs arg [arg ...]] [REDUCE function nargs arg [arg ...]]]
      [SORTBY nargs property [ASC|DESC] [property [ASC|DESC] ...] [MAX num]]
      [APPLY expression AS name]
      [LIMIT offset num]
      [FILTER expression]
      [WITHSCORES]
      [ADDSCORES]
      [SCORER scorer]
      [BM25STD_TANH_FACTOR factor]
      [PARAMS nargs name value [name value ...]]
      [DIALECT dialect]

**Time complexity:** O(N)

**ACL categories:** @ft_search

## Description

Run a search query and perform aggregate transformations on the results.

This command provides aggregation functionality similar to SQL `GROUP BY` operations, allowing you to group search results and apply reduction functions.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using [`FT.CREATE`](./ft.create.md).
</details>

<details open>
<summary><code>query</code></summary>

is text query to search. If it's more than a single word, put it in quotes.
Both `FLAT` and `HNSW` indexes support KNN and `VECTOR_RANGE` queries. HNSW queries can override `EF_RUNTIME` for KNN search and `EPSILON` for range search. A vector distance score alias defined by the query can be referenced by aggregation operations.
Refer to the [Valkey Search query syntax](https://valkey.io/topics/search-query/) for more details.
</details>

## Optional arguments

<details open>
<summary><code>LOAD count field [field ...]</code></summary>

loads additional fields from the document that are not part of the index.

`count` is the number of fields to load.
`field` is the field name to load from the document.
</details>

<details open>
<summary><code>GROUPBY nargs property [property ...] [REDUCE ...]</code></summary>

groups the results according to one or more properties.

`nargs` is the number of properties to group by.
`property` is the property name to group by.

Optionally followed by one or more `REDUCE` clauses that aggregate the grouped results.
</details>

<details open>
<summary><code>REDUCE function nargs arg [arg ...]</code></summary>

applies an aggregate function to the grouped results.

Common functions include:
- `COUNT` - counts the number of records in each group
- `SUM property` - sums the values of the given property
- `MIN property` - finds minimum value
- `MAX property` - finds maximum value
- `AVG property` - calculates average value
- `STDDEV property` - calculates standard deviation

</details>

<details open>
<summary><code>SORTBY nargs property [ASC|DESC] [property [ASC|DESC] ...] [MAX num]</code></summary>

sorts the results by the given properties.

`nargs` is the number of properties to sort by.
`property` is the property name to sort by.
`ASC|DESC` specifies sort order (default is ASC).
`MAX num` limits the number of results.
</details>

<details open>
<summary><code>APPLY expression AS name</code></summary>

applies a 1-to-1 transformation on one or more properties and stores the result as a new property.

`expression` is the transformation expression to apply.
`name` is the alias for the resulting value.
</details>

<details open>
<summary><code>LIMIT offset num</code></summary>

limits the results to the offset and number of results given.

The offset is zero-indexed. Default is 0 10.
</details>

<details open>
<summary><code>FILTER expression</code></summary>

filters the results using a predicate expression, similar to the `WHERE` clause in SQL.

`expression` is the filter predicate to apply after aggregation.
</details>

<details open>
<summary><code>WITHSCORES</code></summary>

is accepted for compatibility with [`FT.SEARCH`](./ft.search.md) but has no effect on `FT.AGGREGATE` — it is silently ignored. To include the score in aggregate output, use `ADDSCORES` instead.
</details>

<details open>
<summary><code>ADDSCORES</code></summary>

adds the document score to each result as the `__score` field. When no `SCORER` is specified, the default BM25STD scorer is used.
</details>

<details open>
<summary><code>SCORER scorer</code></summary>

specifies the scoring function used to compute the score. Supported scorers are `BM25STD`, `BM25STD.NORM`, `BM25STD.TANH`, `TFIDF`, and `TFIDF.DOCNORM`. On its own `SCORER` only sets the scoring function — it does not add a visible score to the output; combine it with `ADDSCORES` to expose the computed score as `__score`. With `BM25STD.TANH`, `BM25STD_TANH_FACTOR` optionally sets the positive integer scaling factor; its default is `4`.
</details>

<details open>
<summary><code>PARAMS nargs name value [name value ...]</code></summary>

defines one or more value parameters that can be referenced in the query.

Similar to [`FT.SEARCH`](./ft.search.md) PARAMS option.
</details>

<details open>
<summary><code>DIALECT dialect</code></summary>

selects the dialect version to use for the query.

`dialect` is the dialect version number.
</details>

## Return

`FT.AGGREGATE` returns an array reply with aggregated results based on the specified grouping and reduction operations.

:::info Limited support
FT.AGGREGATE has partial support in Dragonfly. Some advanced aggregation functions and options may not be fully implemented.
:::

## Examples

<details open>
<summary><b>Group results by category and count</b></summary>

```bash
dragonfly> FT.AGGREGATE products "*" GROUPBY 1 @category REDUCE COUNT 0 AS count
```
</details>

<details open>
<summary><b>Calculate average price by category</b></summary>

```bash
dragonfly> FT.AGGREGATE products "*" GROUPBY 1 @category REDUCE AVG 1 @price AS avg_price
```
</details>

## See also

[`FT.SEARCH`](./ft.search.md) | [`FT.CREATE`](./ft.create.md) | [`FT.HYBRID`](./ft.hybrid.md)

## Related topics

- [Valkey Search](https://valkey.io/topics/search/)
