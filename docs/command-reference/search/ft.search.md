---
description: Searches the index with a query, returning docs or just ids
---

# FT.SEARCH

## Syntax

    FT.SEARCH index query
      [NOCONTENT]
      [RETURN count identifier [AS property] [ identifier [AS property] ...]]
      [SORTBY sortby [ ASC | DESC] [WITHCOUNT]]
      [LIMIT offset num]
      [PARAMS nargs name value [ name value ...]]

**Time complexity:** O(N)

## Description

Search the index with a textual query, returning either documents or just IDs.
For usage, see [examples](#examples) below.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using `FT.CREATE`.
</details>

<details open>
<summary><code>query</code></summary> 

is text query to search. If it's more than a single word, put it in quotes.
Refer to [Query syntax](https://redis.io/docs/interact/search-and-query/query/) for more details.
</details>

## Optional arguments

<details open>
<summary><code>NOCONTENT</code></summary>

returns the document ids and not the content.

This is useful if Dragonfly is storing an index on an external document collection.
</details>

<details open>
<summary><code>RETURN num identifier AS property ...</code></summary>

limits the attributes returned from the document.

`num` is the number of attributes following the keyword. If `num` is 0, it acts like `NOCONTENT`.
`identifier` is either an attribute name (for hashes and JSON) or a JSON Path expression (for JSON).
`property` is an optional name used in the result. If not provided, the `identifier` is used in the result.
</details>

<details open>
<summary><code>SORTBY attribute [ASC|DESC]</code></summary>

orders the results by the value of this attribute.

This applies to both text and numeric attributes.
Attributes needed for `SORTBY` should be declared as `SORTABLE` in the index, in order to be available with very low latency.
Note that this adds memory overhead.
</details>

<details open>
<summary><code>LIMIT first num</code></summary>

limits the results to the offset and number of results given.

Note that the offset is zero-indexed.
The default is 0 10, which returns 10 items starting from the first result.
You can use `LIMIT 0 0` to count the number of documents in the result set without actually returning them.
</details>

<details open>
<summary><code>PARAMS nargs name value</code></summary>

defines one or more value parameters. Each parameter has a name and a value.

You can reference parameters in the `query` by a `$`, followed by the parameter name, for example, `$user`.
Each such reference in the search query to a parameter name is substituted by the corresponding parameter value.
For example, with parameter definition `PARAMS 4 start 2020 end 2021`, the expression `@published_at:[$start $end]` is evaluated to `@published_at:[2020 2021]`.
You cannot reference parameters in the query string where concrete values are not allowed, such as in field names, for example, `@published_at`.
</details>

## Return

`FT.SEARCH` returns an array reply, where the first element is an integer reply of the total number of results, and then array reply pairs of document ids, and array replies of attribute/value pairs.

:::note Notes
- If `NOCONTENT` is given, an array is returned where the first element is the total number of results, and the rest of the members are document ids.
- If a hash expires after the query process starts, the hash is counted in the total number of results, but the key name and content return as null.
:::

## Complexity

`FT.SEARCH` complexity is O(N) for single word queries, where `N` is the number of the results in the result set.
Finding all the documents that have a specific term is O(1).
However, a scan on all those documents is needed to load the documents data from Hash or JSON values and return them.

The time complexity for more complex queries varies, but in general it's proportional to the number of words,
the number of intersection points between them and the number of results in the result set.

## Examples

<details open>
<summary><b>Search for a term in every text attribute</b></summary>

Search for the term "wizard" in every TEXT attribute of an index containing book data.

``` bash
dragonfly> FT.SEARCH books-idx "wizard"
```
</details>

<details open>
<summary><b>Search for a term in title attribute</b></summary>

Search for the term _dogs_ in the `title` attribute.

``` bash
dragonfly> FT.SEARCH books-idx "@title:dogs"
```
</details>

<details open>
<summary><b>Search for books from specific years</b></summary>

Search for books published in 2020 or 2021.

``` bash
dragonfly> FT.SEARCH books-idx "@published_at:[2020 2021]"
```
</details>

<details open>
<summary><b>Search for a book by a term and TAG</b></summary>

Search for books with _space_ in the title that have `science` in the TAG attribute `categories`.

``` bash
dragonfly> FT.SEARCH books-idx "@title:space @categories:{science}"
```
</details>

<details open>
<summary><b>Search for a book by a term but limit the number</b></summary>

Search for books with _Python_ in any `TEXT` attribute, returning 10 results starting with the 11th result in the
entire result set (the offset parameter is zero-based), and return only the `title` attribute for each result.

``` bash
dragonfly> FT.SEARCH books-idx "python" LIMIT 10 10 RETURN 1 title
```
</details>

<details open>
<summary><b>Search for a book by a term and price</b></summary>

Search for books with _Python_ in any `TEXT` attribute, returning the price stored in the original JSON document.

``` bash
dragonfly> FT.SEARCH books-idx "python" RETURN 3 $.book.price AS price
```
</details>

## See also

[`FT.CREATE`](./ft.create.md) | `FT.AGGREGATE` 

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
- [Extensions](https://redis.io/docs/interact/search-and-query/administration/extensions/)
- [Highlighting](https://redis.io/docs/interact/search-and-query/advanced-concepts/highlight/)
- [Query syntax](https://redis.io/docs/interact/search-and-query/query/)
