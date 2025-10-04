---
description: Runs a search query and performs aggregate transformations
---

# FT.AGGREGATE

## Syntax

    FT.AGGREGATE index query
      [LOAD count field [field ...]]
      [GROUPBY nargs property [property ...] [REDUCE function nargs arg [arg ...]] [REDUCE function nargs arg [arg ...]]]
      [SORTBY nargs property [ASC|DESC] [property [ASC|DESC] ...] [MAX num]]
      [LIMIT offset num]
      [PARAMS nargs name value [name value ...]]

**Time complexity:** O(N)

## Description

Run a search query and perform aggregate transformations on the results.

This command provides aggregation functionality similar to SQL GROUP BY operations, allowing you to group search results and apply reduction functions.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using [`FT.CREATE`](./ft.create.md).
</details>

<details open>
<summary><code>query</code></summary>

is text query to search. If it's more than a single word, put it in quotes.
Refer to [query syntax](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/) for more details.
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
<summary><code>LIMIT offset num</code></summary>

limits the results to the offset and number of results given.

The offset is zero-indexed. Default is 0 10.
</details>

<details open>
<summary><code>PARAMS nargs name value [name value ...]</code></summary>

defines one or more value parameters that can be referenced in the query.

Similar to [`FT.SEARCH`](./ft.search.md) PARAMS option.
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

[`FT.SEARCH`](./ft.search.md) | [`FT.CREATE`](./ft.create.md)

## Related topics

- [RediSearch](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/)