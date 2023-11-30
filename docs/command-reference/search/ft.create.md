---
description: Creates an index with the given spec
---

# FT.CREATE

## Syntax

    FT.CREATE index
      [ON HASH | JSON]
      [PREFIX count prefix [prefix ...]]
      SCHEMA field_name [AS alias] TEXT | TAG | NUMERIC | VECTOR [ SORTABLE ]
      [NOINDEX] [ field_name [AS alias] TEXT | TAG | NUMERIC | VECTOR [ SORTABLE ] [NOINDEX] ...]

**Time complexity:** O(K) at creation where K is the number of fields, O(N) if scanning the keyspace is triggered, where N is the number of keys in the keyspace.

## Description

Create an index with the given specification.
For usage, see [examples](#examples) below.

## Required arguments

<a name="index"></a>
<details open>
<summary><code>index</code></summary>

is index name to create.
</details>

<a name="SCHEMA"></a>
<details open>
<summary><code>SCHEMA field_name [AS alias] TEXT | TAG | NUMERIC | VECTOR [ SORTABLE ]</code></summary> 

after the SCHEMA keyword, declares which fields to index:

 - `{identifier}` for hashes, is a field name within the hash.
   For JSON, the identifier is a JSON Path expression.

 - `AS {attribute}` defines the attribute associated to the identifier.
   For example, you can use this feature to alias a complex JSONPath expression with more memorable (and easier to type) name.

Field types are:

 - `TEXT` - Allows searching for words against the text value in this attribute.

 - `TAG` - Allows exact-match queries, such as categories or primary keys, against the value in this attribute. For more information, see [Tag Fields](https://redis.io/docs/interact/search-and-query/advanced-concepts/tags/).

 - `NUMERIC` - Allows numeric range queries against the value in this attribute. See [query syntax docs](https://redis.io/docs/interact/search-and-query/query/) for details on how to use numeric ranges.

 - `VECTOR` - Allows vector similarity queries against the value in this attribute. For more information, see [Vector Fields](https://redis.io/docs/interact/search-and-query/search/vectors/).

:::note About `VECTOR`
- Full documentation on vector options is available [here](https://redis.io/docs/interact/search-and-query/advanced-concepts/vectors/).
- Currently, Dragonfly has limited support for vector options.
- You can specify either the `FLAT` or the `HNSW` index type.
  - For both index types, `DIM`, `DISTANCE_METRIC`, and `INITIAL_CAP` options can be specified.
  - For the `DISTANCE_METRIC` option, only `L2` and `COSINE` are supported.
:::

Field options are:

 - `SORTABLE` - `NUMERIC`, `TAG`, `TEXT` attributes can have an optional **SORTABLE** argument.
    As the user [sorts the results by the value of this attribute](https://redis.io/docs/interact/search-and-query/advanced-concepts/sorting/), the results are available with very low latency.
    Note that his adds memory overhead, so consider not declaring it on large text attributes.
    You can sort an attribute without the `SORTABLE` option, but the latency is not as good as with `SORTABLE`.

:::note About `SORTABLE`
Dragonfly does **not** supporting sorting without the `SORTABLE` option.
:::

 - `NOINDEX` - Attributes can have the `NOINDEX` option, which means they will not be indexed. This is useful in conjunction with `SORTABLE`, to create attributes whose update using PARTIAL will not cause full reindexing of the document. If an attribute has NOINDEX and doesn't have SORTABLE, it will just be ignored by the index.

</details>

## Optional arguments

<a name="ON"></a>
<details open>
<summary><code>ON data_type</code></summary>

currently supports HASH (default) and JSON.
</details>

<a name="PREFIX"></a>
<details open>
<summary><code>PREFIX count prefix</code></summary> 

tells the index which keys it should index.
You can add several prefixes to index.
Because the argument is optional, the default is `*` (all keys).

:::note About `PREFIX`
Currently, Dragonfly supports only one prefix (i.e., `PREFIX 1`), if the `PREFIX` option is used.
:::
</details>

## Return

`FT.CREATE` returns a simple string reply `OK` if executed correctly, or an error reply otherwise.

## Examples

<details open>
<summary><b>Create index on HASH</b></summary>

Create an index that stores the title, publication date, and categories of blog post hashes whose keys start with `blog:post:` (i.e., `blog:post:1`).

``` bash
dragonfly> FT.CREATE idx ON HASH PREFIX 1 blog:post: SCHEMA title TEXT SORTABLE published_at NUMERIC SORTABLE category TAG SORTABLE
OK
```

Index the `sku` attribute from a hash as both a `TEXT` and as `TAG`:

``` bash
dragonfly> FT.CREATE idx ON HASH PREFIX 1 blog:post: SCHEMA sku AS sku_text TEXT sku AS sku_tag TAG SORTABLE
```

</details>

<details open>
<summary><b>Create index on JSON</b></summary>

Index a JSON document using a JSON Path expression.

``` bash
dragonfly> FT.CREATE idx ON JSON SCHEMA $.title AS title TEXT $.categories AS categories TAG
```
</details>

## See also

`FT.ALTER` | [`FT.DROPINDEX`](./ft.dropindex.md) 

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
- [Hash](../hashes/hset.md)
- [JSON](../json/json.set.md)
