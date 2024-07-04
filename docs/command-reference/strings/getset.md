---
description: Learn how Redis GETSET sets a new value for a key & returns the old value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETSET

<PageTitle title="Redis GETSET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GETSET` command in Redis is used to atomically set a key to a new value and return the old value stored at that key. This is particularly useful in scenarios where you need to update a value and simultaneously retrieve its previous state, such as implementing counters or managing session data.

## Syntax

```
GETSET key value
```

## Parameter Explanations

- **key**: The name of the key whose value you want to set and retrieve. It must be a string.
- **value**: The new value you want to assign to the key. This can be any string.

## Return Values

The `GETSET` command returns the old value stored at the specified key before the update. If the key did not exist, it returns `nil`.

Example outputs:

- If the key exists: `"old_value"`
- If the key does not exist: `(nil)`

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> GETSET mykey "World"
"Hello"
dragonfly> GET mykey
"World"
dragonfly> GETSET anotherkey "test"
(nil)
dragonfly> GET anotherkey
"test"
```

## Best Practices

- Use `GETSET` when you need to ensure atomicity between getting and setting a value to avoid race conditions.
- Be aware that `GETSET` only works with string values. If you need similar functionality with complex data types, consider other commands or structures.

## Common Mistakes

- Using `GETSET` on non-string data types. This command is intended for string values only.
- Assuming `GETSET` creates the key if it doesn't exist. While it sets the value, it won't show up in a `GETSET` operation until the first set.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GETSET` will return `nil` and create the key with the new value.

### Can I use `GETSET` with data types other than strings?

No, `GETSET` is designed to work with string values only. For other data types, consider using appropriate Redis commands tailored to those types.
