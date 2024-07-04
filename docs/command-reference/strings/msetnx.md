---
description: Understand how to use Redis MSETNX to set multiple keys only if they don't exist.
---

import PageTitle from '@site/src/components/PageTitle';

# MSETNX

<PageTitle title="Redis MSETNX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MSETNX` command in Redis sets multiple key-value pairs at once, but only if none of the specified keys already exist. It's useful for ensuring atomicity when initializing values that shouldn't overwrite existing data.

## Syntax

```plaintext
MSETNX key1 value1 [key2 value2 ...]
```

## Parameter Explanations

- **key1, value1, key2, value2, ...**: Pairs of keys and values to set. All provided keys will be set to their respective values, but only if none of them already exist in the database.

## Return Values

- **(integer) 1**: If the keys were set successfully because none of them existed.
- **(integer) 0**: If no keys were set because at least one of the specified keys already exists.

## Code Examples

```cli
dragonfly> MSETNX key1 "value1" key2 "value2"
(integer) 1
dragonfly> MSETNX key1 "newvalue1" key3 "value3"
(integer) 0
dragonfly> GET key1
"value1"
dragonfly> GET key2
"value2"
dragonfly> GET key3
(nil)
```

## Best Practices

- Use `MSETNX` when you need to ensure that a batch of keys is set atomically without overwriting existing data.
- Combine `MSETNX` with other commands like `EXISTS` if more complex conditional logic is needed before setting values.

## Common Mistakes

- Assuming `MSETNX` will partially apply values if some keys don't already exist. The command is atomic; it either sets all keys or none.
- Forgetting that `MSETNX` only works if none of the specified keys exist—meaning even one existing key will cause the entire operation to fail.

## FAQs

### How does `MSETNX` differ from `MSET`?

While `MSET` sets multiple keys regardless of whether they already exist, `MSETNX` ensures none of the specified keys exist before setting any values.

### Can `MSETNX` set a single key-value pair?

Yes, but it's typically used for multiple key-value pairs. For single key-value operations, using `SETNX` is more straightforward.
