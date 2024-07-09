---
description: "Learn how to use Redis HVALS command to fetch all the values in a hash. Simplify your data retrieval tasks with this command."
---

import PageTitle from '@site/src/components/PageTitle';

# HVALS

<PageTitle title="Redis HVALS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HVALS` command in Redis is used to retrieve all the values stored in a hash. This command is particularly useful when you need to access all the values without knowing their corresponding fields. Typical use cases include aggregating data for reporting, extracting information for processing, or simply displaying all associated values of a particular key.

## Syntax

```plaintext
HVALS key
```

## Parameter Explanations

- **key**: The name of the hash from which you want to retrieve all values. It must be an existing hash key; otherwise, an empty list is returned.

## Return Values

The `HVALS` command returns a list of values contained in the hash. If the hash does not exist, it returns an empty list.

### Example Outputs:

1. When the hash exists:

   ```plaintext
   1) "value1"
   2) "value2"
   3) "value3"
   ```

2. When the hash does not exist:
   ```plaintext
   (empty list or set)
   ```

## Code Examples

```cli
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HVALS myhash
1) "Hello"
2) "World"
```

## Best Practices

- Ensure that the key provided is indeed a hash type to avoid unexpected results.
- Utilize the `HEXISTS` command before `HVALS` if there's uncertainty about the existence of the key.

## Common Mistakes

- Using `HVALS` on a non-hash key will result in an error. Always ensure the key type is a hash.
  ```cli
  dragonfly> SET mystring "value"
  OK
  dragonfly> HVALS mystring
  (error) WRONGTYPE Operation against a key holding the wrong kind of value
  ```

## FAQs

### What happens if the hash key does not exist?

If the specified hash key does not exist, `HVALS` will return an empty list.

### Can I use `HVALS` with large hashes?

Yes, but be cautious as retrieving a large number of values can be resource-intensive. For large data sets, consider using pagination or other methods to manage data retrieval efficiently.
