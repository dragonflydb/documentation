---
description: Searches the index with a query, returning docs or just IDs
---

import PageTitle from '@site/src/components/PageTitle';

# FT.SEARCH

<PageTitle title="Redis FT.SEARCH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`FT.SEARCH` is a command in the RediSearch module of Redis. It performs full-text searches on indexes created with RediSearch, allowing for complex querying capabilities similar to those found in search engines like Elasticsearch. Typical use cases include searching through large datasets, filtering results based on multiple criteria, and leveraging advanced text search features such as stemming, phonetics, and synonyms.

## Syntax

```
FT.SEARCH index query [NOCONTENT] [VERBATIM] [NOSTOPWORDS] [WITHSCORES] [WITHPAYLOADS] [WITHSORTKEYS] [FILTER field min max] [GEOFILTER field lon lat radius m|km|mi|ft] [INKEYS num key ...] [INFIELDS num field ...] [RETURN num field ...] [SUMMARIZE ...] [HIGHLIGHT ...] [SLOP slop] [INORDER] [LANGUAGE lang] [EXPANDER expander] [SCORER scorer] [PAYLOAD payload] [SORTBY field [ASC|DESC]] [LIMIT offset num]
```

## Parameter Explanations

- **index**: The name of the index to search.
- **query**: The search query string.
- **NOCONTENT**: If set, returns only document IDs and not the content.
- **VERBATIM**: Disables query expansion and applies verbatim matching.
- **NOSTOPWORDS**: Prevents stopwords from being excluded when processing the query.
- **WITHSCORES**: Returns scores along with documents.
- **WITHPAYLOADS**: Includes payloads with returned documents.
- **WITHSORTKEYS**: Returns the sorting keys.
- **FILTER field min max**: Filters results based on numeric range in the specified field.
- **GEOFILTER field lon lat radius unit**: Filters results based on geographical location.
- **INKEYS num key ...**: Limits the search to a specific set of keys.
- **INFIELDS num field ...**: Limits the search to specific fields.
- **RETURN num field ...**: Specifies which fields to return.
- **SUMMARIZE ...**: Creates snippets of the text.
- **HIGHLIGHT ...**: Highlights terms in the results.
- **SLOP slop**: Sets the maximum number of intervening non-query terms allowed between query terms.
- **INORDER**: Requires terms to appear in the same order as the query.
- **LANGUAGE lang**: Specifies the language used for stemming.
- **EXPANDER expander**: Defines custom query expander.
- **SCORER scorer**: Specifies a custom scoring function.
- **PAYLOAD payload**: Adds a payload to the query.
- **SORTBY field [ASC|DESC]**: Sorts results by the specified field.
- **LIMIT offset num**: Limits the number of results returned starting at the offset.

## Return Values

Returns an array where the first element is the total number of documents that match the query, followed by document-specific information. If `WITHSCORES` is used, each document will include its score.

Example outputs:

- Without options:

  ```
  1) (integer) 2
  2) "doc1"
  3) "doc2"
  ```

- With `WITHSCORES`:
  ```
  1) (integer) 2
  2) "doc1"
  3) "1.0"
  4) "doc2"
  5) "0.8"
  ```

## Code Examples

```cli
dragonfly> FT.SEARCH myIndex "hello world" LIMIT 0 10
1) (integer) 2
2) "doc1"
3) "doc2"

dragonfly> FT.SEARCH myIndex "hello" WITHSCORES
1) (integer) 2
2) "doc1"
3) "1.0"
4) "doc2"
5) "0.8"

dragonfly> FT.SEARCH myIndex "world" NOCONTENT
1) (integer) 1
2) "doc2"
```

## Best Practices

- Index your data appropriately to optimize search performance.
- Regularly update your indexes to reflect the latest data.
- Use `NOCONTENT` when you only need document ids to save bandwidth.

## Common Mistakes

- Forgetting to create an index before using `FT.SEARCH`.
- Using the wrong syntax or omitting required parameters.
- Not handling the return value structure correctly, leading to
