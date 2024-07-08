---
description: Creates an index with the given spec
---

import PageTitle from '@site/src/components/PageTitle';

# FT.CREATE

<PageTitle title="Redis FT.CREATE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `FT.CREATE` command in Redis is used to create an index for full-text search capabilities provided by the RediSearch module. This command is essential for setting up a new index on one or more fields of your documents, enabling efficient search queries. Typical use cases include searching through large datasets, filtering documents based on specific criteria, and implementing advanced search features in applications.

## Syntax

```plaintext
FT.CREATE {index} [ON {structure}] [PREFIX {count} {prefix}] [FILTER {filter}] [LANGUAGE {default_lang}] [SCORE {default_score}] [SCHEMA {schema}]
```

## Parameter Explanations

- `{index}`: Name of the index.
- `[ON {structure}]`: The data structure to index (e.g., HASH, JSON). Default is HASH.
- `[PREFIX {count} {prefix}]`: One or more key prefixes to index.
- `[FILTER {filter}]`: A filter expression to limit the indexed documents.
- `[LANGUAGE {default_lang}]`: Default language used for stemming.
- `[SCORE {default_score}]`: Default score for ranking the results.
- `[SCHEMA {schema}]`: Define fields and their types to be indexed.

## Return Values

The command returns `OK` if the index is created successfully.

## Code Examples

```cli
dragonfly> FT.CREATE myIndex ON HASH PREFIX 1 doc: SCHEMA title TEXT WEIGHT 5.0 body TEXT url TEXT
OK
dragonfly> HSET doc:1 title "Hello World" body "This is a test document." url "http://example.com"
(integer) 3
dragonfly> HSET doc:2 title "Redis Search" body "Full-text search with Redis and RediSearch." url "http://redis.io"
(integer) 3
dragonfly> FT.SEARCH myIndex "test"
1) (integer) 1
2) "doc:1"
3) 1) "title"
   2) "Hello World"
   3) "body"
   4) "This is a test document."
   5) "url"
   6) "http://example.com"
```

## Best Practices

- Define appropriate weights for different fields in the `SCHEMA` to improve the relevance of search results.
- Use the `PREFIX` option to limit the index to specific keys, which can enhance performance.
- Regularly update and optimize your index as your dataset grows.

## Common Mistakes

- Forgetting to specify the correct structure (HASH or JSON) when creating an index.
- Not defining a schema, leading to inefficient searches.
- Using overly broad prefixes, which may slow down indexing and search operations.

### What happens if I forget to specify a prefix?

If you don't specify a prefix, all keys in the database will be indexed, potentially causing performance issues.

### Can I modify an existing index?

No, once an index is created, its schema cannot be altered. You would need to drop the index and create it again with the desired schema.
