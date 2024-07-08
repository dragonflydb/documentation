---
description: Returns information and statistics on the index
---

import PageTitle from '@site/src/components/PageTitle';

# FT.INFO

<PageTitle title="Redis FT.INFO Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`FT.INFO` is a Redis command used with the RediSearch module. It provides detailed information about an index, which includes its configuration, internal data structures, and memory usage. This command is typically used for monitoring and debugging purposes to gain insights into the performance and efficiency of the search indexes.

## Syntax

```plaintext
FT.INFO <index>
```

## Parameter Explanations

- `<index>`: The name of the index for which information is requested. This parameter is required and must be a valid index created in RediSearch.

## Return Values

The command returns a bulk string reply that contains various fields with details about the specified index. Each field provides specific metrics or configuration settings such as document count, term count, memory usage, and more. The output is presented in a key-value format.

Example possible outputs:

- `index_name`: Name of the index.
- `index_options`: Options set while creating the index.
- `fields`: List of fields indexed.
- `num_docs`: Number of documents indexed.
- `max_doc_id`: Maximum document ID.
- `num_terms`: Number of terms.
- `num_records`: Number of records.
- `inverted_sz_mb`: Size of inverted index in megabytes.
- `bytes_per_term_avg`: Average bytes per term.
- `indexing`: Status of indexing.

## Code Examples

```cli
dragonfly> FT.CREATE myIndex SCHEMA title TEXT WEIGHT 5.0 body TEXT URL TEXT
OK
dragonfly> FT.INFO myIndex
1) "index_name"
2) "myIndex"
3) "index_options"
4) (empty array)
5) "fields"
6) 1) 1) "title"
      2) "type"
      3) "TEXT"
      4) "WEIGHT"
      5) "5.0"
   2) 1) "body"
      2) "type"
      3) "TEXT"
   3) 1) "URL"
      2) "type"
      3) "TEXT"
7) "num_docs"
8) "0"
9) "max_doc_id"
10) "0"
11) "num_terms"
12) "0"
13) "num_records"
14) "0"
15) "inverted_sz_mb"
16) "0.000000"
17) "bytes_per_term_avg"
18) "0.000000"
19) "indexing"
20) "Idle"
```

## Best Practices

- Use `FT.INFO` periodically to monitor the health and performance of your indexes.
- Analyze the memory usage fields to optimize and potentially reconfigure your indexes for better performance.

## Common Mistakes

- Not specifying a valid index name will result in an error. Ensure the index exists before querying it with `FT.INFO`.

## FAQs

### What kind of data can I see using FT.INFO?

You can see a variety of data such as the number of documents, memory usage, configuration options, and detailed statistics about the index structure.

### Can I use FT.INFO on any Redis database?

No, `FT.INFO` is specific to the RediSearch module and only applies to indexes managed by this module.
