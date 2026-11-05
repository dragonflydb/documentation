---
description: Query syntax of FT.SEARCH, FT.AGGREGATE, FT.HYBRID and FT.PROFILE in Dragonfly, and how it differs from Valkey Search
sidebar_position: 1
---

# Query syntax

The `query` argument of [`FT.SEARCH`](./ft.search.md), [`FT.AGGREGATE`](./ft.aggregate.md) and [`FT.PROFILE`](./ft.profile.md), and the `SEARCH` query and `VSIM` `FILTER` expression of [`FT.HYBRID`](./ft.hybrid.md), use the syntax described on this page.
It differs from the syntax documented for Valkey Search in several places; see [Differences from Valkey Search](#differences-from-valkey-search).

Pass the query as one argument, in quotes if it contains spaces.

## Quick reference

| Syntax | Matches |
|:--|:--|
| `word` | Documents that contain `word` in any `TEXT` attribute |
| `@title:word` | `word` in the `title` attribute |
| `a b` | Documents that match both `a` and `b` (AND) |
| `a \| b` | Documents that match `a`, `b` or both (OR) |
| `-a` | Documents that do not match `a` (NOT) |
| `(a \| b) c` | Grouping |
| `"a b"`, `'a b'` | The words next to each other, in this order |
| `"a b"~2` | The words in this order, with up to 2 other words between them |
| `pre*`, `*suf`, `*inf*` | Words that start with, end with, or contain the text |
| `w'p?th*n'` | Words that match a glob pattern |
| `~a` | Does not filter; with scoring, documents that match `a` rank higher |
| `a=>{$weight: 2}` | Doubles the score that `a` contributes |
| `@price:[10 20]`, `@price:[(10 +inf]` | Values in a numeric range |
| `@tags:{a \| b*}` | Documents with one of the tags |
| `@loc:[13.405 52.52 10 km]` | Points within a radius |
| `@attr:*` | Documents that have a value for `attr` |
| `*` | All documents |
| `$name` | The value of `name` from `PARAMS` |
| `*=>[KNN 10 @vec $q]` | The 10 documents with the nearest vectors |
| `@vec:[VECTOR_RANGE 0.5 $q]` | Documents with a vector within a distance |

## Words and attributes

- A word matches documents that contain it in any `TEXT` attribute. Matching is case-insensitive, and words are stemmed: `learning` matches `learn`, and `runs` matches `running`. Attributes declared with `NOSTEM` are matched without stemming.
- A word does not search `TAG`, `NUMERIC`, `GEO` or `VECTOR` attributes; use the operators below for them.
- `@attr:` limits the next word, phrase, pattern or parenthesized group to the attribute `attr`. `@title:python basics` matches `python` in `title` and `basics` in any `TEXT` attribute; `@title:(python basics)` matches both words in `title`.
- Attribute names are case-sensitive. Refer to a JSON path by its `AS` name from `FT.CREATE`.
- Stopwords are dropped from the query: `the python` is the same as `python`, and a query made of stopwords only matches nothing. Set the stopword list with `STOPWORDS` in [`FT.CREATE`](./ft.create.md).
- A word that belongs to a synonym group, created with [`FT.SYNUPDATE`](./ft.synupdate.md), also matches the other words of the group.
- `AS`, `KNN`, `EF_RUNTIME` and `VECTOR_RANGE` are keywords in any letter case. As plain words or tag values, they fail with `ERR Query syntax error`; to search for one, quote it: `"knn"` or `@tags:{"knn"}`.

## Logical operators

- A space between two conditions means AND, `|` means OR, and `-` before a condition means NOT.
- AND binds tighter than OR: `a b | c` is `(a b) | c`. `-` applies to the next condition only: `-a b` is `(-a) b`. Use parentheses to group conditions.
- NOT also matches documents that have no value for the attribute: `-@tags:{bread}` returns documents without tags too.
- `*` matches all documents. It cannot be combined with other conditions: `* python` is a syntax error. Its main use is as the filter of a [KNN query](#knn).
- `@attr:*` matches the documents that have a value for `attr`, and `-@attr:*` matches the documents that have none. This works for every attribute type except `HNSW` vectors, where it fails with `ERR Invalid field: <name>`.

## Phrases

- `"a b c"` matches documents in which the words appear next to each other, in this order, in one `TEXT` attribute. Single quotes work the same way: `'a b c'`.
- `"a b c"~N` allows up to `N` other words between consecutive words of the phrase; the order is still required. Write `~N` right after the closing quote: after a space, `~` is the [optional operator](#optional-words-and-weights).
- Phrase words are not stemmed: `"runs"` does not match `running`, while `runs` does. A `TEXT` attribute without `NOSTEM` also indexes the stem of every word, so a phrase word that is itself a stem matches the other forms: `"run"` matches `running`.
- Stopwords are ignored both in the phrase and in the indexed text: `"running of the man"` matches `The running man`.

## Prefix, suffix, infix and glob patterns

- `pre*` matches words that start with `pre`, `*suf` words that end with `suf`, and `*inf*` words that contain `inf`.
- `w'pattern'` or `w"pattern"` is a glob pattern: `*` matches any sequence of characters and `?` matches one character. Only a lowercase `w` starts a pattern.
- Patterns are not stemmed, but they also match the stems in the index: `*thon` matches `pythonic`, whose stem is `python`. They work in `TEXT` attributes and inside [tag](#tags) braces.
- Suffix and infix patterns work on every `TEXT` attribute; `WITHSUFFIXTRIE` in `FT.CREATE` makes them faster.

## Optional words and weights

- `~condition` makes the condition optional: it never removes documents from the result, but when scores are computed, documents that match it get a higher score. A query made only of optional conditions, such as `~java`, matches all documents.
- `condition=>{$weight: w}` multiplies the score that the condition contributes by `w`, a number from `0` to `1000000`. It can follow a word, phrase, pattern, parenthesized group or `@attr:` condition. Spaces inside the braces and a trailing `;` are allowed.
- Scores are computed only with `WITHSCORES` or `SCORER` in [`FT.SEARCH`](./ft.search.md), and with `ADDSCORES` or `SCORER` in [`FT.AGGREGATE`](./ft.aggregate.md), which ignores `WITHSCORES`. The `SEARCH` query of [`FT.HYBRID`](./ft.hybrid.md) is always scored.

## Numeric ranges

- `@attr:[min max]` matches values from `min` to `max`, both included. A `(` before a bound excludes it: `[(10 20]`, `[10 (20]`. `-inf`, `+inf` and `inf` give open ranges. A comma may separate the bounds: `[10,20]`.
- Bounds are integers or decimals with an optional sign, such as `-5.5` or `.5`. Exponent notation, such as `1e3`, is a syntax error.
- Write a single value as a range: `@price:[10 10]`. `@price:10` fails with `ERR Wrong access type for field: price`.
- Negate a range with `-@price:[10 20]` or `@price:-[10 20]`. Ranges cannot be grouped in parentheses: write `@price:[0 10] | @price:[20 30]`, not `@price:([0 10] | [20 30])`.

## Tags

- `@attr:{value}` matches documents that have this tag, and `@attr:{a | b}` documents that have any of the tags. A value can also be a prefix (`{co*}`), a suffix (`{*fee}`), an infix (`{*off*}`) or a glob pattern (`{w'c?ffee'}`).
- Tags are compared case-insensitively unless the attribute is declared with `CASESENSITIVE`.
- Escape spaces and punctuation in a value with a backslash, or quote the whole value: `{hello\ world}` or `{"hello world"}`, `{c\.d}` or `{"c.d"}`. Unescaped, they are a syntax error. Letters, digits, `_`, non-ASCII characters and a `:` between other characters need no escaping.
- A [parameter](#parameters) is used as a tag value as it is: `@tags:{$tag}` with `PARAMS 2 tag c.d` needs no escaping.

## Geo radius

- `@attr:[lon lat radius unit]` matches points within `radius` of the point at longitude `lon` and latitude `lat`. `unit` is `m`, `km`, `mi` or `ft`, in any letter case; `radius` is an integer or a decimal.
- Write `lon` and `lat` with a decimal point or a sign: `@loc:[13.0 52.0 100 km]` works, while `@loc:[13 52 100 km]` is a syntax error. Separate the four values with spaces only.
- A `GEO` value must be a `lon,lat` string with the longitude first, such as `13.405,52.52`. A document whose `GEO` value cannot be parsed or is out of range, such as `13.40 52.52` or `52.52,113.36`, is not indexed at all.

## Parameters

- `$name` is replaced with the value of `name` from the `PARAMS` argument. The value is used as one token and is not parsed again: `pyth*` is searched as a literal word, and punctuation in a tag value needs no escaping.
- In a numeric range and as a geo radius, the value must be an integer from 0 to 4294967295: a value such as `15.5` or `-5` is a syntax error. Geo coordinates and attribute names cannot be parameters.
- The `KNN` count, `EF_RUNTIME`, the `VECTOR_RANGE` radius, the distance name after `AS` and the values in `=>{...}` attribute blocks can be parameters.
- A parameter that is missing from `PARAMS` fails with `ERR Query syntax error`.

## Vector search

### KNN

```text
filter=>[KNN k @attr $vector [EF_RUNTIME ef] [AS alias]]=>{$EF_RUNTIME: ef; $YIELD_DISTANCE_AS: alias}
```

- `filter` is `*` or any other query, but it cannot contain a `VECTOR_RANGE` on an `HNSW` attribute. `KNN` returns the `k` documents among its matches whose vectors are nearest to the query vector, sorted by distance. The KNN clause comes last, at the top level of the query, and only once.
- `$vector` is a parameter that holds the query vector as little-endian bytes of the attribute's `TYPE`, for example 4 bytes per dimension for `FLOAT32`. A vector with the wrong number of dimensions fails with `ERR Wrong vector index dimensions, got: 1, expected: 2`; a value whose length is not a multiple of the element size fails with `ERR Parse error of vector parameters` on an `HNSW` attribute and returns no results on a `FLAT` attribute.
- Each result includes its distance, named `alias`, or `__<attr>_score` (for example `__vec_score`) without `AS`. With `RETURN`, the distance is returned only if its name is listed.
- `EF_RUNTIME` sets the HNSW search breadth for this query. `FLAT` attributes are always searched exhaustively.
- The attribute block after `]` is optional. It takes `$EF_RUNTIME` and `$YIELD_DISTANCE_AS`, separated by `;`, and its values override `EF_RUNTIME` and `AS` in the brackets.
- Keywords and attribute block names are case-insensitive.

### VECTOR_RANGE

```text
@attr:[VECTOR_RANGE radius $vector]=>{$YIELD_DISTANCE_AS: alias; $EPSILON: epsilon}
```

- Matches documents whose vectors are within `radius` of the query vector. A negative radius fails with `ERR VECTOR_RANGE radius must be non-negative, got: -1`.
- The distance follows the attribute's `DISTANCE_METRIC`: the Euclidean distance for `L2`, 1 minus the dot product for `IP`, and 1 minus the cosine similarity for `COSINE`.
- The attribute block is optional. `$YIELD_DISTANCE_AS` returns the distance under `alias`. Results are not always ordered by distance; add `SORTBY alias` to `FT.SEARCH`.
- `$EPSILON`, a number greater than 0 and up to 1000000, overrides the attribute's `EPSILON` for this search. It is supported only on `HNSW` attributes: on a `FLAT` attribute, the query fails with `ERR EPSILON is supported only for HNSW VECTOR_RANGE`.
- On an `HNSW` attribute, a query can contain one `VECTOR_RANGE` only, and only AND can combine it with other conditions. Otherwise, it fails with `ERR Combining multiple VECTOR_RANGE clauses with an HNSW index is not supported` or `ERR Combining VECTOR_RANGE with OR/NOT is not supported on HNSW indexes`.

## Words with punctuation

- Inside a word, the characters `. , ! # & = < > ^ ? + / '` join the parts on both sides. The joined word matches like its parts in parentheses: `@email:example.com` is `@email:(example com)`, so every part must be in `email`, in any order and position. It matches both `john.doe@example.com` and `com@example.org`. To require the parts next to each other and in order, use a phrase: `@email:"example.com"`.
- These characters are dropped at the start and end of a word: `.com` is `com`, and `C++` is `C`.
- `*` cannot be next to one of these characters: `*.com` and `example.*` are syntax errors. `*example.com*` is accepted, but it joins `*example` and `com*`; it is not an infix search for `example.com`.
- `- | ~ *` keep their meaning as operators inside a word. For example, `well-known` means `well -known` and matches documents that contain `well` but not `known`; search for the phrase `"well-known"` instead.
- `@ : ; % [ ] { }` and the backtick are syntax errors inside a word, so quote an e-mail address as a phrase: `"john.doe@example.com"`. `(`, `)` and `$` keep their meaning: `python(x)` is `python (x)`, and in `python$b`, `$b` is a [parameter](#parameters).
- A backslash makes the next character part of the word. `TEXT` values are split at punctuation when they are indexed, so an escaped word such as `well\-known` matches nothing in them unless the stored text escapes the character too; escaping is useful in tag values.
- A decimal number such as `3.14` is one query word, but `TEXT` attributes index it as the words `3` and `14`, so it matches nothing. Search for the phrase `"3.14"` instead.

## Errors

- `ERR Query syntax error`: the query cannot be parsed. `FT.PROFILE` returns `ERR query syntax error`. In `FT.HYBRID`, an invalid `SEARCH` query returns `ERR Query syntax error in SEARCH clause`, and an invalid `VSIM` `FILTER` expression returns `ERR KNN query error for VSIM field` for a `FLAT` vector attribute and `ERR Query syntax error in VSIM FILTER clause` for an `HNSW` one.
- `ERR Invalid field: <name>`: the attribute is not in the schema, or is an `HNSW` vector attribute used where `HNSW` is not supported, such as `@vec:*` or a `VECTOR_RANGE` in the filter of a KNN query on the same attribute.
- `ERR Wrong access type for field: <name>`: the operator does not fit the attribute type, such as a word on a `NUMERIC` attribute.
- `ERR Query string is too long, max length is 10240 bytes`: the query is longer than `search.query-string-bytes`, which you can change with [`FT.CONFIG`](./ft.config.md).

Only `FT.SEARCH` and `FT.PROFILE` return the `Invalid field` and `Wrong access type` errors. `FT.AGGREGATE` returns no rows instead, and in `FT.HYBRID` the `SEARCH` query or `FILTER` expression that contains the error matches nothing.

## Differences from Valkey Search

The [Valkey Search query syntax](https://valkey.io/topics/search-query/) page describes a related but different dialect. Compared with it, Dragonfly:

- Has no fuzzy matching: `%term%` is a syntax error.
- Does not accept `AS` or `EF_RUNTIME` inside the `VECTOR_RANGE` brackets, such as `@vec:[VECTOR_RANGE 0.5 $q AS dist]`, or `HYBRID_POLICY` inside the KNN brackets. Both are syntax errors; name the distance with `=>{$YIELD_DISTANCE_AS: dist}` instead.
- Requires spaces in tag values to be escaped or quoted: `@color:{hello world}` is a syntax error.
- Does not accept exponent notation in numeric ranges, such as `@price:[-inf (1e2]`.
- Uses the Euclidean distance for `L2`, where Valkey Search uses the squared distance, so `VECTOR_RANGE` radii differ: a radius of `0.5` in Dragonfly corresponds to `0.25` in Valkey Search.
- Supports `$weight`, and applies `$EPSILON` on `HNSW` attributes.
- Accepts an attribute block after the KNN brackets: `=>{$EF_RUNTIME: ef; $YIELD_DISTANCE_AS: alias}`.
- Runs suffix and infix patterns without `WITHSUFFIXTRIE`.
- Ignores stopwords inside phrases.
- Has no `SLOP`, `INORDER` or `VERBATIM` options: `FT.SEARCH` skips them without an error, and `FT.AGGREGATE` fails with `ERR Unknown clause: SLOP`. Use a phrase with slop instead.
- Supports syntax that the Valkey page does not describe: geo radius, infix and glob patterns, optional words, phrase slop, `@attr:*`, and punctuation inside words.

## Examples

Each example creates its own index and data.
Without `SORTBY` or `WITHSCORES`, the order of the returned document IDs depends on how the keys are distributed across shards, so it can differ on your server.

<details open>
<summary><b>Words, attributes and logical operators</b></summary>

`@body:learning` matches `Learn`, because words are stemmed.

```shell
dragonfly> FT.CREATE books ON HASH PREFIX 1 book: SCHEMA title TEXT body TEXT
OK
dragonfly> HSET book:1 title "Python basics" body "Learn Python programming fast"
(integer) 2
dragonfly> HSET book:2 title "Advanced Python" body "Python design patterns"
(integer) 2
dragonfly> HSET book:3 title "Java basics" body "Learn Java programming"
(integer) 2
dragonfly> FT.SEARCH books python NOCONTENT
1) (integer) 2
2) "book:2"
3) "book:1"
dragonfly> FT.SEARCH books @title:basics NOCONTENT
1) (integer) 2
2) "book:1"
3) "book:3"
dragonfly> FT.SEARCH books "python basics" NOCONTENT
1) (integer) 1
2) "book:1"
dragonfly> FT.SEARCH books "python | java" NOCONTENT
1) (integer) 3
2) "book:2"
3) "book:1"
4) "book:3"
dragonfly> FT.SEARCH books "basics -java" NOCONTENT
1) (integer) 1
2) "book:1"
dragonfly> FT.SEARCH books "@title:(python | java) @body:learning" NOCONTENT
1) (integer) 2
2) "book:1"
3) "book:3"
```
</details>

<details open>
<summary><b>Phrases and patterns</b></summary>

The exact phrase `"learn programming"` matches nothing, because another word stands between the two words in both documents. The slop `~1` allows it.

```shell
dragonfly> FT.CREATE books ON HASH PREFIX 1 book: SCHEMA title TEXT body TEXT
OK
dragonfly> HSET book:1 title "Python basics" body "Learn Python programming fast"
(integer) 2
dragonfly> HSET book:2 title "Advanced Python" body "Python design patterns"
(integer) 2
dragonfly> HSET book:3 title "Java basics" body "Learn Java programming"
(integer) 2
dragonfly> FT.SEARCH books '"python programming"' NOCONTENT
1) (integer) 1
2) "book:1"
dragonfly> FT.SEARCH books '"learn programming"' NOCONTENT
1) (integer) 0
dragonfly> FT.SEARCH books '"learn programming"~1' NOCONTENT
1) (integer) 2
2) "book:1"
3) "book:3"
dragonfly> FT.SEARCH books pyth* NOCONTENT
1) (integer) 2
2) "book:2"
3) "book:1"
dragonfly> FT.SEARCH books *thon NOCONTENT
1) (integer) 2
2) "book:2"
3) "book:1"
dragonfly> FT.SEARCH books *ytho* NOCONTENT
1) (integer) 2
2) "book:2"
3) "book:1"
dragonfly> FT.SEARCH books "w'?ava'" NOCONTENT
1) (integer) 1
2) "book:3"
```
</details>

<details open>
<summary><b>Optional words and weights</b></summary>

`~java` keeps the same two matches as `learn` and raises the score of `book:3`, which contains `java`.
A weight of 3 on `python` moves both Python books above `book:3`.

```shell
dragonfly> FT.CREATE books ON HASH PREFIX 1 book: SCHEMA title TEXT body TEXT
OK
dragonfly> HSET book:1 title "Python basics" body "Learn Python programming fast"
(integer) 2
dragonfly> HSET book:2 title "Advanced Python" body "Python design patterns"
(integer) 2
dragonfly> HSET book:3 title "Java basics" body "Learn Java programming"
(integer) 2
dragonfly> FT.SEARCH books learn WITHSCORES NOCONTENT
1) (integer) 2
2) "book:3"
3) "0.485274"
4) "book:1"
5) "0.442174"
dragonfly> FT.SEARCH books "learn ~java" WITHSCORES NOCONTENT
1) (integer) 2
2) "book:3"
3) "2.4788"
4) "book:1"
5) "0.442174"
dragonfly> FT.SEARCH books "python | java" WITHSCORES NOCONTENT
1) (integer) 3
2) "book:3"
3) "1.99353"
4) "book:2"
5) "0.955278"
6) "book:1"
7) "0.912178"
dragonfly> FT.SEARCH books "python=>{$weight: 3} | java" WITHSCORES NOCONTENT
1) (integer) 3
2) "book:2"
3) "2.86583"
4) "book:1"
5) "2.73653"
6) "book:3"
7) "1.99353"
```
</details>

<details open>
<summary><b>Numeric, tag and geo conditions</b></summary>

`shop:1` and `shop:2` are within 30 km of central Berlin. `shop:4` has no tags.

```shell
dragonfly> FT.CREATE shops ON HASH PREFIX 1 shop: SCHEMA name TEXT tags TAG price NUMERIC loc GEO
OK
dragonfly> HSET shop:1 name "Berlin cafe" tags coffee,wifi price 4.5 loc 13.405,52.52
(integer) 4
dragonfly> HSET shop:2 name "Potsdam bakery" tags bread,coffee price 2 loc 13.06,52.39
(integer) 4
dragonfly> HSET shop:3 name "Paris bistro" tags wine price 12 loc 2.35,48.86
(integer) 4
dragonfly> HSET shop:4 name "Street stand" price 1
(integer) 2
dragonfly> FT.SEARCH shops "@price:[2 5]" NOCONTENT
1) (integer) 2
2) "shop:2"
3) "shop:1"
dragonfly> FT.SEARCH shops "@price:[(2 +inf]" NOCONTENT
1) (integer) 2
2) "shop:3"
3) "shop:1"
dragonfly> FT.SEARCH shops "@tags:{coffee | wine}" NOCONTENT
1) (integer) 3
2) "shop:3"
3) "shop:2"
4) "shop:1"
dragonfly> FT.SEARCH shops "@tags:{co*} -@tags:{bread}" NOCONTENT
1) (integer) 1
2) "shop:1"
dragonfly> FT.SEARCH shops "@loc:[13.405 52.52 30 km]" NOCONTENT
1) (integer) 2
2) "shop:2"
3) "shop:1"
dragonfly> FT.SEARCH shops -@tags:* NOCONTENT
1) (integer) 1
2) "shop:4"
```
</details>

<details open>
<summary><b>Parameters</b></summary>

```shell
dragonfly> FT.CREATE shops ON HASH PREFIX 1 shop: SCHEMA name TEXT tags TAG price NUMERIC loc GEO
OK
dragonfly> HSET shop:1 name "Berlin cafe" tags coffee,wifi price 4.5 loc 13.405,52.52
(integer) 4
dragonfly> HSET shop:2 name "Potsdam bakery" tags bread,coffee price 2 loc 13.06,52.39
(integer) 4
dragonfly> HSET shop:3 name "Paris bistro" tags wine price 12 loc 2.35,48.86
(integer) 4
dragonfly> FT.SEARCH shops "@tags:{$tag} @price:[0 $max]" NOCONTENT PARAMS 4 tag coffee max 3
1) (integer) 1
2) "shop:2"
dragonfly> FT.SEARCH shops "@loc:[13.405 52.52 $radius km]" NOCONTENT PARAMS 2 radius 30
1) (integer) 2
2) "shop:2"
3) "shop:1"
```
</details>

<details open>
<summary><b>Punctuation and tag escaping</b></summary>

`@email:example.com` also matches `com@example.org`, which contains both words; the phrase matches only the adjacent pair.

```shell
dragonfly> FT.CREATE users ON HASH PREFIX 1 user: SCHEMA email TEXT tags TAG
OK
dragonfly> HSET user:1 email john.doe@example.com tags "c.d,hello world"
(integer) 2
dragonfly> HSET user:2 email com@example.org tags a-b
(integer) 2
dragonfly> FT.SEARCH users @email:example.com NOCONTENT
1) (integer) 2
2) "user:1"
3) "user:2"
dragonfly> FT.SEARCH users '@email:"example.com"' NOCONTENT
1) (integer) 1
2) "user:1"
dragonfly> FT.SEARCH users '@email:"john.doe@example.com"' NOCONTENT
1) (integer) 1
2) "user:1"
dragonfly> FT.SEARCH users @tags:{c\.d} NOCONTENT
1) (integer) 1
2) "user:1"
dragonfly> FT.SEARCH users '@tags:{"hello world"}' NOCONTENT
1) (integer) 1
2) "user:1"
dragonfly> FT.SEARCH users @tags:{a\-b} NOCONTENT
1) (integer) 1
2) "user:2"
dragonfly> FT.SEARCH users @tags:{$tag} NOCONTENT PARAMS 2 tag c.d
1) (integer) 1
2) "user:1"
```
</details>

<details open>
<summary><b>Vector search</b></summary>

The vectors are stored in JSON documents as arrays. `$q` is the query vector `[1.0, 0.0]` as `FLOAT32` little-endian bytes, written with redis-cli `\x` escapes.
The `L2` distances are Euclidean: `item:2`, with the vector `[0.8, 0.6]`, is about 0.632 away.

```shell
dragonfly> FT.CREATE items ON JSON PREFIX 1 item: SCHEMA $.name AS name TEXT $.color AS color TAG $.vec AS vec VECTOR HNSW 6 TYPE FLOAT32 DIM 2 DISTANCE_METRIC L2
OK
dragonfly> JSON.SET item:1 $ '{"name":"red shoes","color":"red","vec":[1,0]}'
OK
dragonfly> JSON.SET item:2 $ '{"name":"blue shoes","color":"blue","vec":[0.8,0.6]}'
OK
dragonfly> JSON.SET item:3 $ '{"name":"red dress","color":"red","vec":[0,1]}'
OK
dragonfly> FT.SEARCH items "*=>[KNN 2 @vec $q AS dist]" RETURN 1 dist PARAMS 2 q "\x00\x00\x80?\x00\x00\x00\x00"
1) (integer) 2
2) "item:1"
3) 1) "dist"
   2) "0"
4) "item:2"
5) 1) "dist"
   2) "0.632455587387085"
dragonfly> FT.SEARCH items "@color:{red}=>[KNN 2 @vec $q]=>{$EF_RUNTIME: 50; $YIELD_DISTANCE_AS: dist}" RETURN 1 dist PARAMS 2 q "\x00\x00\x80?\x00\x00\x00\x00"
1) (integer) 2
2) "item:1"
3) 1) "dist"
   2) "0"
4) "item:3"
5) 1) "dist"
   2) "1.4142135381698608"
dragonfly> FT.SEARCH items "@vec:[VECTOR_RANGE 0.7 $q]=>{$YIELD_DISTANCE_AS: dist; $EPSILON: 0.1}" SORTBY dist RETURN 1 dist PARAMS 2 q "\x00\x00\x80?\x00\x00\x00\x00"
1) (integer) 2
2) "item:1"
3) 1) "dist"
   2) "0"
4) "item:2"
5) 1) "dist"
   2) "0.632455587387085"
```
</details>

## See also

[`FT.SEARCH`](./ft.search.md) | [`FT.AGGREGATE`](./ft.aggregate.md) | [`FT.HYBRID`](./ft.hybrid.md) | [`FT.PROFILE`](./ft.profile.md) | [`FT.CREATE`](./ft.create.md) | [`FT.SYNUPDATE`](./ft.synupdate.md)

## Related topics

- [Valkey Search](https://valkey.io/topics/search/)
- [Valkey Search query syntax](https://valkey.io/topics/search-query/)
