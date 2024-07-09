---
description: "Learn Redis RENAMENX command to rename a key, only if the new key does not exist."
---

import PageTitle from '@site/src/components/PageTitle';

# RENAMENX

<PageTitle title="Redis RENAMENX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `RENAMENX` command in Redis is used to rename a key only if the new key does not already exist. This ensures that you do not accidentally overwrite an existing key. Typical use cases include safely renaming keys in situations where key conflicts need to be avoided.

## Syntax

```plaintext
RENAMENX oldkey newkey
```

## Parameter Explanations

- **oldkey**: The current key you want to rename.
- **newkey**: The new name for the key, which must not already exist in the database.

## Return Values

`RENAMENX` returns an integer:

- `1`: If the key was successfully renamed.
- `0`: If the new key already exists and the rename operation was not performed.

## Code Examples

```cli
dragonfly> SET mykey "value"
OK
dragonfly> RENAMENX mykey mynewkey
(integer) 1
dragonfly> GET mynewkey
"value"
dragonfly> SET anotherkey "anothervalue"
OK
dragonfly> RENAMENX mynewkey anotherkey
(integer) 0
dragonfly> GET mynewkey
"value"
dragonfly> GET anotherkey
"anothervalue"
```

## Best Practices

- Always ensure that the `newkey` you are renaming to does not exist to avoid unexpected behaviors.
- Make use of `EXISTS newkey` before calling `RENAMENX` to verify the key's non-existence if needed.

## Common Mistakes

- Attempting to rename a key to an existing key without checking: This will cause the operation to fail (`0` as the return value).
- Confusing `RENAMENX` with `RENAME`, which will overwrite the new key regardless of its existence.

## FAQs

### Can I use RENAMENX to swap keys?

No, `RENAMENX` does not support swapping keys. It only renames a key if the new key does not exist.

### What happens if the old key does not exist?

If the `oldkey` does not exist, `RENAMENX` behaves like other commands operating on non-existent keys and returns 0. No key is created or modified in this case.
