---
description: Creates an index with the given spec
---

# FT.CREATE

## Syntax

    FT.CREATE index
      [ON HASH | JSON]
      [PREFIX count prefix [prefix ...]]
      [STOPWORDS count [words...]]
      SCHEMA field_name [AS alias] TEXT | TAG | NUMERIC | VECTOR | GEO [ SORTABLE ]
      [NOINDEX] [ field_name [AS alias] TEXT | TAG | NUMERIC | VECTOR | GEO [ SORTABLE ] [NOINDEX] ...]

**Time complexity:** O(K) at creation where K is the number of fields, O(N) if scanning the keyspace is triggered, where N is the number of keys in the keyspace.

## Description

Create an index with the given specification.
For usage, see [examples](#examples) below.

## Required arguments

<a name="index"></a>
<details open>
<summary><code>index</code></summary>

is index name to create. If such index already exists, returns an error reply.
</details>

<a name="SCHEMA"></a>
<details open>
<summary><code>SCHEMA field_name [AS alias] TEXT | TAG | NUMERIC | VECTOR [ SORTABLE ]</code></summary> 

after the SCHEMA keyword, declares which fields to index:

 - `{identifier}` is the name of the field to index:
   - For Hash values, identifier is a field name within the Hash.
   - For JSON values, the identifier is a JSONPath expression.

 - `AS {attribute}` defines the attribute associated to the identifier.
   For example, you can use this feature to alias a complex JSONPath expression with more memorable (and easier to type) name.

Field types are:

 - `TEXT [WITHSUFFIXTRIE]` - Allows searching for words against the text value in this attribute.
   * `WITHSUFFIXTRIE` - builds a suffix trie for efficient suffix and infix queries.

 - `TAG [SEPARATOR {char}] [CASESENSITIVE] [WITHSUFFIXTRIE]` - Allows exact-match queries, such as categories or primary keys, against the value in this attribute.
   * `SEPARATOR {char}` - indicates how text is split into individual tags. Default is `,`.
   * `CASESENSITIVE` - preserve original case for tags. Default is case insensitive.
   * `WITHSUFFIXTRIE` - builds a suffix trie for efficient suffix and infix queries.
   For more information, see [tag fields](https://redis.io/docs/interact/search-and-query/advanced-concepts/tags/).

 - `NUMERIC [BLOCKSIZE {size}]` - Allows numeric range queries against the value in this attribute.
   * `BLOCKSIZE {size}` - block size for the range tree data structure. Default is optimized based on data size.
   See [query syntax](https://redis.io/docs/interact/search-and-query/query/) for details on how to use numeric ranges.

 - `VECTOR` - Allows vector similarity queries against the value in this attribute.
   For more information, see [vector fields](https://redis.io/docs/interact/search-and-query/search/vectors/).

 - `GEO` - Allows geographic range queries against the value in this attribute.

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
Dragonfly does **not** support sorting without the `SORTABLE` option.
:::

 - `NOINDEX` - Attributes can have the `NOINDEX` option, which means they will not be indexed. This is useful in conjunction with `SORTABLE`, to create attributes whose update using PARTIAL will not cause full reindexing of the document. If an attribute has NOINDEX and doesn't have SORTABLE, it will just be ignored by the index.

:::note About ignored field options
The following field options are accepted but ignored for compatibility with Redis:
- `UNF`, `NOSTEM` - ignored without arguments
- `WEIGHT`, `PHONETIC` - ignored with their arguments
- `INDEXMISSING`, `INDEXEMPTY` - ignored without warning
:::

</details>

## Optional arguments

<a name="ON"></a>
<details open>
<summary><code>ON data_type</code></summary>

currently supports `HASH` (default) and `JSON`.
</details>

<a name="PREFIX"></a>
<details open>
<summary><code>PREFIX count prefix</code></summary> 

tells the index which keys it should index.
You can add several prefixes to index.
Because the argument is optional, the default is `*` (all keys).

:::note About `PREFIX`
Currently, Dragonfly supports only one prefix (i.e., `PREFIX 1 my_prefix`), if the `PREFIX` option is used.
:::
</details>

<a name="STOPWORDS"></a>
<details open>
<summary><code>STOPWORDS count [words...]</code></summary>

sets the index's stopword list to the given list of stopwords.
Stopwords are common words (like "the", "a", "is") that are typically ignored during indexing and searching.

If `count` is 0, the index will have no stopwords.
If `count` is greater than 0, the following `count` arguments will be treated as stopwords.

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
OK
```

Create an index with custom TAG separator and case-sensitive matching:

``` bash
dragonfly> FT.CREATE products_idx ON HASH PREFIX 1 product: SCHEMA categories TAG SEPARATOR "|" CASESENSITIVE SORTABLE price NUMERIC BLOCKSIZE 64 description TEXT WITHSUFFIXTRIE
OK
```

Create an index with custom stopwords:

``` bash
dragonfly> FT.CREATE articles_idx ON HASH PREFIX 1 article: STOPWORDS 3 the a is SCHEMA title TEXT content TEXT NOINDEX
OK
```

</details>

<details open>
<summary><b>Create index on JSON</b></summary>

Index a JSON document using a JSONPath expression.

``` bash
dragonfly> FT.CREATE idx ON JSON SCHEMA $.title AS title TEXT $.categories AS categories TAG
```
</details>

## See also

[`FT.SEARCH`](./ft.search.md) | [`FT.DROPINDEX`](./ft.dropindex.md)

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
- [Hash](../hashes/hset.md)
- [JSON](../json/json.set.md)
