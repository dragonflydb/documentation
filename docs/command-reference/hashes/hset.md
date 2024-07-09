---
description: "Learn how to use Redis HSET command to set the value of a hash field. A fundamental function for data update tasks."
---

import PageTitle from '@site/src/components/PageTitle';

# HSET

<PageTitle title="Redis HSET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HSET` command in Redis is used to set the value of a field in a hash. If the hash does not exist, it is created. This command is typically used for storing objects or records where each field represents an attribute of the object.

## Syntax

```plaintext
HSET key field value [field value ...]
```

## Parameter Explanations

- `key`: The name of the hash.
- `field`: The field within the hash whose value you want to set.
- `value`: The value to assign to the field.

Multiple field-value pairs can be specified in a single `HSET` command.

## Return Values

The command returns an integer representing the number of fields that were added to the hash, not including fields that already existed.

- If a new field is added: `(integer) 1`
- If an existing field's value is updated: `(integer) 0`

## Code Examples

```cli
dragonfly> HSET myhash field1 "value1"
(integer) 1
dragonfly> HSET myhash field2 "value2"
(integer) 1
dragonfly> HSET myhash field2 "new_value2"
(integer) 0
dragonfly> HGETALL myhash
1) "field1"
2) "value1"
3) "field2"
4) "new_value2"
```

## Best Practices

- Use meaningful and consistent naming conventions for keys and fields to keep data organized and understandable.
- Consider using TTL (`EXPIRE`) for hashes if the data should only persist for a specific period.

## Common Mistakes

- Not checking if a field already exists before setting a value might lead to unintended data overwrites.
- Passing incorrect types for field or value can cause unexpected behavior.

## FAQs

### What happens if I `HSET` a value to a non-existing hash?

A new hash will be created automatically with the specified field-value pair.

### Can `HSET` handle multiple fields at once?

Yes, you can set multiple field-value pairs by chaining them in the command.

### Will `HSET` overwrite existing fields?

Yes, if the field already exists, its value will be overwritten.
