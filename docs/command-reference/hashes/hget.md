---
description: "Learn how to use Redis HGET command to retrieve the value of a hash field. Perfect for data fetching tasks."
---

import PageTitle from '@site/src/components/PageTitle';

# HGET

<PageTitle title="Redis HGET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HGET` command in Redis is used to retrieve the value associated with a given field in a hash stored at a specific key. It's commonly used when working with hash data structures to fetch individual field values efficiently.

## Syntax

```
HGET key field
```

## Parameter Explanations

- **key**: The name of the hash from which you want to retrieve the value.
- **field**: The specific field whose value you want to fetch within the hash.

## Return Values

- The command returns the value associated with the specified field in the hash, or `nil` if the field does not exist.

Example:

```
"someValue"
(nil)
```

## Code Examples

```cli
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HGET myhash field1
"Hello"
dragonfly> HGET myhash field2
"World"
dragonfly> HGET myhash field3
(nil)
```

## Best Practices

- Ensure that the key exists and is of type hash before using `HGET`.
- Consider using `HEXISTS` to check if a field exists before attempting to get its value.

## Common Mistakes

- Using `HGET` on a key that does not hold a hash value results in an error.
- Trying to fetch a value from a non-existent field will return `nil`.

## FAQs

### What happens if I use HGET on a non-hash key?

You will receive an error indicating that the operation against a key holding the wrong kind of value.

### Can I use HGET to fetch multiple fields at once?

No, `HGET` retrieves the value for a single field. To fetch multiple fields, consider using `HMGET`.
