---
description: "Learn how to use Redis HGETALL command to fetch all fields and values of a hash. Streamline your data retrieval with ease."
---

import PageTitle from '@site/src/components/PageTitle';

# HGETALL

<PageTitle title="Redis HGETALL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HGETALL` command in Redis is used to retrieve all the fields and values of a hash stored at a specific key. This command is particularly useful when you need to get a complete view of a hash's contents, such as retrieving user profile data or configuration settings stored in a hash.

## Syntax

```
HGETALL key
```

## Parameter Explanations

- `key`: The name of the hash from which you want to retrieve all the fields and values. It is a string that identifies the hash.

## Return Values

The `HGETALL` command returns an array of strings representing the fields and values of the hash. If the hash does not exist, it returns an empty array.

Example outputs:

1. If the hash exists:

   ```
   1) "field1"
   2) "value1"
   3) "field2"
   4) "value2"
   ```

2. If the hash does not exist:
   ```
   (empty array)
   ```

## Code Examples

```cli
dragonfly> HMSET myhash field1 "value1" field2 "value2"
OK
dragonfly> HGETALL myhash
1) "field1"
2) "value1"
3) "field2"
4) "value2"
dragonfly> HGETALL nonexistinghash
(empty array)
```

## Best Practices

- Ensure the key for the hash exists before using `HGETALL` to avoid unexpected empty results.
- When dealing with large hashes, consider whether fetching all fields and values at once is efficient for your application's performance requirements.

## Common Mistakes

- Using `HGETALL` on a key that is not a hash type will return an error.

## FAQs

### What happens if I use `HGETALL` on a key that is not a hash?

You will receive an error message indicating that the key is of the wrong type.

### Is there a way to fetch only specific fields from a hash?

Yes, you can use the `HMGET` command to retrieve specific fields from a hash.
