---
description: "Learn to use Redis KEYS command to find keys that match a pattern."
---

import PageTitle from '@site/src/components/PageTitle';

# KEYS

<PageTitle title="Redis KEYS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `KEYS` command in Redis is used to find all keys matching a given pattern. It is particularly useful for debugging or discovering key names within your database, especially in development environments. However, it should be used sparingly in production due to its potential impact on performance.

## Syntax

```plaintext
KEYS pattern
```

## Parameter Explanations

- `pattern`: A glob-style pattern to match keys against. Patterns can include special characters:
  - `*` matches zero or more characters.
  - `?` matches exactly one character.
  - `[abc]` matches any one of the characters inside the brackets.
  - `[a-z]` matches any character in the range.

## Return Values

The `KEYS` command returns an array of keys that match the specified pattern.

Example:

```plaintext
1) "key1"
2) "key2"
3) "anotherkey"
```

If no keys match, it returns an empty list.

## Code Examples

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> SET anotherkey "value3"
OK
dragonfly> KEYS key*
1) "key1"
2) "key2"
dragonfly> KEYS *key
1) "anotherkey"
dragonfly> KEYS k?y1
1) "key1"
```

## Best Practices

- **Use in Development:** The `KEYS` command is best used in development or debugging scenarios due to its potential to cause high latency by scanning the entire keyspace.
- **Alternative Commands:** In production, prefer using `SCAN` as it performs incremental iterations over the keyspace, being more memory and CPU efficient.
- **Pattern Specificity:** Be specific with the patterns to minimize the number of keys returned and reduce overhead.

## Common Mistakes

- **Large Databases:** Running `KEYS` on a large dataset can block the server and degrade performance. Use it cautiously.
- **Misunderstanding Patterns:** Ensure the correct use of wildcard characters in patterns to avoid unexpected results.

## FAQs

### How does `KEYS` impact Redis performance?

Using `KEYS` on a large dataset can block the Redis server, leading to increased latency and potential downtime for other operations. It scans the entire keyspace, which can be resource-intensive.

### What are the alternatives to `KEYS` for safer production use?

The `SCAN` command is recommended for iterating through large datasets incrementally. It allows you to process keys in batches without blocking the server.
