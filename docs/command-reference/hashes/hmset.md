---
description: "Learn how to use Redis HMSET command to set multiple hash fields to multiple values. Excellent for bulk data operations."
---

import PageTitle from '@site/src/components/PageTitle';

# HMSET

<PageTitle title="Redis HMSET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`HMSET` is a Redis command used to set multiple fields in a hash stored at a key. This command is useful when you need to store or update multiple related data points under a single key, such as user profiles, configuration settings, or other structured data.

## Syntax

```cli
HMSET key field1 value1 [field2 value2 ...]
```

## Parameter Explanations

- **`key`**: The name of the hash where the fields are to be set.
- **`field1` `value1`**: The first field-value pair to set in the hash.
- **`field2` `value2`** (optional): Additional field-value pairs to set in the hash.

## Return Values

`HMSET` returns a simple string reply indicating success.

Example:

```cli
"OK"
```

## Code Examples

```cli
dragonfly> HMSET user:1000 username "john_doe" age "30" city "New York"
"OK"
dragonfly> HGETALL user:1000
1) "username"
2) "john_doe"
3) "age"
4) "30"
5) "city"
6) "New York"
```

## Best Practices

- Use descriptive and consistent naming conventions for keys and fields to maintain clarity.
- If possible, prefer `HSET` over `HMSET`, as the latter is deprecated since Redis 4.0. Instead of `HMSET`, use multiple `HSET` operations.

## Common Mistakes

### Using HMSET on an already existing key with conflicting data type

Make sure the key does not hold a non-hash value, or `HMSET` will return an error.

```cli
dragonfly> SET mystring "a string"
"OK"
dragonfly> HMSET mystring field1 "value1"
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```

## FAQs

### What happens if one of the fields already exists?

If a field already exists, `HMSET` will overwrite its value without returning an error.

### Is HMSET atomic?

Yes, `HMSET` is an atomic operation, meaning all field-value pairs are set simultaneously.
