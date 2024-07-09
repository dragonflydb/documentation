---
description: "Learn how to use Redis HKEYS command to fetch all the keys in a hash. Make large dataset navigation simpler and faster."
---

import PageTitle from '@site/src/components/PageTitle';

# HKEYS

<PageTitle title="Redis HKEYS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HKEYS` command in Redis is used to retrieve all the keys (fields) in a hash stored at a specified key. This command is particularly useful when you need to inspect the structure of a hash or iterate over its fields for further processing.

## Syntax

```plaintext
HKEYS key
```

## Parameter Explanations

- `key`: The name of the hash from which to retrieve the fields. If the hash does not exist, an empty list is returned.

## Return Values

The `HKEYS` command returns a list of strings, each representing a field in the hash.

### Example Outputs

- If the hash contains fields: `["field1", "field2", "field3"]`
- If the hash is empty or does not exist: `[]`

## Code Examples

```cli
dragonfly> HSET myhash field1 "value1" field2 "value2"
(integer) 2
dragonfly> HKEYS myhash
1) "field1"
2) "field2"
dragonfly> HDEL myhash field1
(integer) 1
dragonfly> HKEYS myhash
1) "field2"
dragonfly> DEL myhash
(integer) 1
dragonfly> HKEYS myhash
(empty array)
```

## Best Practices

- Ensure that the key exists and is of type hash before calling `HKEYS` to avoid unnecessary operations.
- Combine `HKEYS` with other hash commands like `HGETALL` or `HVALS` for more comprehensive data manipulations.

## Common Mistakes

- Attempting to use `HKEYS` on a key that is not a hash will result in an error. Always verify the data type if unsure.
- Forgetting to check if the hash is empty can lead to assumptions that the key doesn't exist.

## FAQs

### What happens if the key does not exist?

If the specified key does not exist, `HKEYS` returns an empty list.

### Can I use `HKEYS` on non-hash data types?

No, using `HKEYS` on a key that holds a non-hash value results in an error.
