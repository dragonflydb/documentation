---
description: Uses SEARCH command to collect performance info
---

import PageTitle from '@site/src/components/PageTitle';

# FT.PROFILE

<PageTitle title="Redis FT.PROFILE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`FT.PROFILE` is a command in Redis used with the RedisSearch module to allow detailed profiling of queries. This command helps in understanding the performance characteristics and execution details of full-text search queries, making it useful for optimizing query performance and debugging complex searches.

## Syntax

```plaintext
FT.PROFILE {index} {QUERY|SEARCH} [query_args]
```

## Parameter Explanations

- **index**: The name of the index you are querying.
- **QUERY|SEARCH**: Determines whether you are running a free-text query (`QUERY`) or a `SEARCH`.
- **query_args**: Additional arguments that specify the search terms and options for the query.

## Return Values

The command returns a detailed report on the execution of the query, including various stages and steps taken by the query engine. This includes parsing time, execution time for different parts of the query, and how results were filtered and returned.

### Example Output

```plaintext
1) "Parsing"
2)  (execution details)
3) "Pipeline"
4)  (stage details)
5) "Total Execution Time"
6)  (time in milliseconds)
```

## Code Examples

```cli
dragonfly> FT.CREATE myIdx SCHEMA title TEXT WEIGHT 5.0 body TEXT
OK
dragonfly> FT.PROFILE myIdx SEARCH QUERY "hello world"
1) "Parsing"
2)  "Execution time: 0.123 ms"
3) "Pipeline"
4)  "Stage 1: Term matching"
5)    "Matched documents: 10"
6) "Total Execution Time"
7)  "Execution time: 1.456 ms"
```

## Best Practices

- Use `FT.PROFILE` in development or staging environments to fine-tune query performance before deploying to production.
- Compare profiling reports over time to identify any regressions in query performance.

## Common Mistakes

- Using `FT.PROFILE` in a high-traffic production environment can impact performance due to its detailed logging nature.
- Not fully understanding the output can lead to misinterpretation. It's beneficial to familiarize yourself with the typical stages and times involved in your specific queries.

## FAQs

### What is the difference between QUERY and SEARCH in FT.PROFILE?

`QUERY` allows for more complex free-text searches, while `SEARCH` is typically used for structured searches within the index.

### Can I use FT.PROFILE to profile aggregation queries?

Currently, `FT.PROFILE` is designed for profiling `QUERY` and `SEARCH` commands. Profiling for aggregation might require different approaches or tools.
