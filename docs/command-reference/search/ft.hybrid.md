---
description: Runs a hybrid search that combines a full-text query with vector similarity and merges the two rankings
---

# FT.HYBRID

## Syntax

    FT.HYBRID index
      SEARCH query [SCORER scorer] [YIELD_SCORE_AS name]
      VSIM @vector_field $param
        [KNN k [EF_RUNTIME ef] [SHARD_K_RATIO ratio]]
        [RANGE radius [EPSILON epsilon]]
        [FILTER filter]
        [YIELD_SCORE_AS name]
      [COMBINE RRF [nargs] [CONSTANT constant] [WINDOW window] [YIELD_SCORE_AS name]]
      [COMBINE LINEAR [nargs] [ALPHA alpha] [BETA beta] [YIELD_SCORE_AS name]]
      [SCORER scorer]
      [LOAD count field [AS alias] ...]
      [LIMIT offset num]
      [PARAMS nargs name value [name value ...]]

**Time complexity:** O(N) to run the text query (N = documents matching the query) plus O(K) for the vector search (K = candidates examined), and O(M·log(M)) to merge and rank the combined set of M unique candidates.

**ACL categories:** @ft_search

## Description

`FT.HYBRID` runs a **full-text query and a vector-similarity query together** and merges their two ranked result lists into a single ranking. It is useful when lexical relevance (keyword matching) and semantic similarity (vector distance) should both influence the final order — for example, retrieval-augmented generation and semantic product search.

The command has two mandatory parts:

- a `SEARCH` clause that runs a normal full-text query (the same query syntax as [`FT.SEARCH`](./ft.search.md)); and
- a `VSIM` clause that runs a vector search (`KNN` nearest-neighbor or `RANGE`) against a vector field.

The two result sets are then merged with a `COMBINE` strategy: **Reciprocal Rank Fusion (`RRF`, the default)** or a weighted **`LINEAR`** combination of the normalized scores.

`FT.HYBRID` is a Dragonfly-specific extension.

## Required arguments

<details open>
<summary><code>index</code></summary>

is the index name. You must first create the index with [`FT.CREATE`](./ft.create.md), and it must contain both the TEXT field(s) used by the query and the VECTOR field used by `VSIM`.
</details>

<details open>
<summary><code>SEARCH query</code></summary>

is the full-text query, using the same [query syntax](https://redis.io/docs/latest/develop/interact/search-and-query/query/) as `FT.SEARCH`. If the query is more than a single word, put it in quotes.
</details>

<details open>
<summary><code>VSIM @vector_field $param</code></summary>

is the vector-search clause. `@vector_field` is the VECTOR field to search (it must start with `@`), and `$param` is the name of the query-vector parameter (it must start with `$`); the actual vector blob is supplied through `PARAMS`.
</details>

## Optional arguments

<details open>
<summary><code>SCORER scorer</code></summary>

selects the scoring function for the text query. Supported scorers are `BM25STD`, `TFIDF`, and `TFIDF.DOCNORM`. May be given inside the `SEARCH` clause or as a trailing option.
</details>

<details open>
<summary><code>KNN k [EF_RUNTIME ef] [SHARD_K_RATIO ratio]</code></summary>

returns the `k` nearest neighbors of the query vector. `EF_RUNTIME` sets the HNSW search breadth (larger is more accurate but slower); `SHARD_K_RATIO` multiplies the number of candidates fetched per shard. `KNN` and `RANGE` are mutually exclusive.
</details>

<details open>
<summary><code>RANGE radius [EPSILON epsilon]</code></summary>

returns every vector within `radius` distance of the query vector instead of a fixed `k`. `EPSILON` is accepted but currently ignored. `RANGE` cannot be combined with `FILTER`.
</details>

<details open>
<summary><code>FILTER filter</code></summary>

applies a pre-filter expression to the vector search. Cannot be combined with `RANGE`.
</details>

<details open>
<summary><code>YIELD_SCORE_AS name</code></summary>

exposes a score in the reply under the field `name`. It can be set independently for the text part (inside `SEARCH`), the vector part (inside `VSIM`), and the combined score (inside `COMBINE`).
</details>

<details open>
<summary><code>COMBINE RRF [nargs] [CONSTANT constant] [WINDOW window] [YIELD_SCORE_AS name]</code></summary>

merges the two rankings with Reciprocal Rank Fusion — this is the **default** when no `COMBINE` clause is given. `CONSTANT` is the RRF constant (default `60`) and `WINDOW` limits how many ranks per list are fused (default `0`, meaning no limit). `nargs` is the number of arguments in the block.
</details>

<details open>
<summary><code>COMBINE LINEAR [nargs] [ALPHA alpha] [BETA beta] [YIELD_SCORE_AS name]</code></summary>

merges the two rankings as a weighted sum of the min-max-normalized scores: `ALPHA` weights the text score and `BETA` weights the vector similarity (both default `0.5`). `nargs` is the number of arguments in the block.
</details>

<details open>
<summary><code>LOAD count field [AS alias] ...</code></summary>

returns the listed document fields for each result (optionally aliased with `AS`). Use `LOAD *` to return all fields. Without `LOAD`, each result contains only its key (`__key`) and the combined score.
</details>

<details open>
<summary><code>LIMIT offset num</code></summary>

paginates the merged results, returning `num` documents starting at `offset`. Defaults to offset `0` and `10` results. The total may not exceed the server's `MAXSEARCHRESULTS` limit.
</details>

<details open>
<summary><code>PARAMS nargs name value [name value ...]</code></summary>

binds query parameters referenced in the command — most importantly the query vector referenced by `$param` in the `VSIM` clause. `nargs` is the number of name/value words that follow.
</details>

## Return

`FT.HYBRID` returns a map reply with four fields:

- `total_results` — the total number of documents matched across the text and vector pipelines.
- `results` — an array of matches. Without `LOAD`, each entry contains `__key` and the combined score under `__score` (or under the `COMBINE` `YIELD_SCORE_AS` alias). With `LOAD`, the requested fields are returned instead. Any text/vector `YIELD_SCORE_AS` scores are added too, but only for documents that were present in that pipeline.
- `warnings` — an array of warning strings (empty when there are none).
- `execution_time` — the server-side execution time, in milliseconds.

The combined score is computed by the active `COMBINE` method (`RRF` by default, otherwise `LINEAR`).

## Examples

First, create an index with a TEXT field and a VECTOR field, and add a few documents (each `vec` field holds a binary FLOAT32 vector):

``` bash
dragonfly> FT.CREATE idx ON HASH PREFIX 1 doc: SCHEMA title TEXT vec VECTOR FLAT 6 TYPE FLOAT32 DIM 2 DISTANCE_METRIC L2
OK
```

<details open>
<summary><b>Basic hybrid search (default RRF)</b></summary>

Combine the text query `running` with a nearest-neighbor vector search and fuse the rankings with the default Reciprocal Rank Fusion. `$q` is a binary FLOAT32 little-endian vector passed via `PARAMS` (here the 2-dimensional vector `[1.0, 0.0]`).

``` bash
dragonfly> FT.HYBRID idx SEARCH "running" VSIM @vec $q KNN 3 PARAMS 2 q "\x00\x00\x80?\x00\x00\x00\x00"
1) "total_results"
2) (integer) 3
3) "results"
4) 1) 1) "__key"
      2) "doc:1"
      3) "__score"
      4) "0.0327869"
   2) 1) "__key"
      2) "doc:2"
      3) "__score"
      4) "0.0322581"
   3) 1) "__key"
      2) "doc:3"
      3) "__score"
      4) "0.015873"
5) "warnings"
6) (empty array)
7) "execution_time"
8) "0.527124"
```
</details>

<details open>
<summary><b>Load fields and yield every score</b></summary>

Return the `title` field and expose the text score (`tscore`), the vector similarity (`vscore`), and the combined RRF score (`cscore`). Score aliases are omitted for documents that did not appear in that pipeline — `doc:3` does not match the text query, so it has no `tscore`.

``` bash
dragonfly> FT.HYBRID idx SEARCH "running" YIELD_SCORE_AS tscore VSIM @vec $q KNN 3 YIELD_SCORE_AS vscore COMBINE RRF 0 YIELD_SCORE_AS cscore LOAD 1 title PARAMS 2 q "\x00\x00\x80?\x00\x00\x00\x00"
1) "total_results"
2) (integer) 3
3) "results"
4) 1) 1) "tscore"
      2) "0.426395"
      3) "title"
      4) "red running shoes"
      5) "cscore"
      6) "0.0327869"
      7) "vscore"
      8) "1"
   2) 1) "tscore"
      2) "0.426395"
      3) "title"
      4) "blue running shoes"
      5) "cscore"
      6) "0.0322581"
      7) "vscore"
      8) "0.980392"
   3) 1) "title"
      2) "red dress"
      3) "cscore"
      4) "0.015873"
      5) "vscore"
      6) "0.333333"
5) "warnings"
6) (empty array)
7) "execution_time"
8) "2.053453"
```
</details>

<details open>
<summary><b>Weighted linear combination</b></summary>

Use a `LINEAR` combination that weights the text score at `0.7` and the vector similarity at `0.3`. Scores are min-max normalized before weighting, so the best match scores `1` and the worst scores `0`.

``` bash
dragonfly> FT.HYBRID idx SEARCH "running" VSIM @vec $q KNN 3 COMBINE LINEAR 4 ALPHA 0.7 BETA 0.3 PARAMS 2 q "\x00\x00\x80?\x00\x00\x00\x00"
1) "total_results"
2) (integer) 3
3) "results"
4) 1) 1) "__key"
      2) "doc:1"
      3) "__score"
      4) "1"
   2) 1) "__key"
      2) "doc:2"
      3) "__score"
      4) "0.97"
   3) 1) "__key"
      2) "doc:3"
      3) "__score"
      4) "0"
5) "warnings"
6) (empty array)
7) "execution_time"
8) "0.362457"
```
</details>

## See also

[`FT.SEARCH`](./ft.search.md) | [`FT.AGGREGATE`](./ft.aggregate.md) | [`FT.CREATE`](./ft.create.md)

## Related topics

- [RediSearch](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/)
