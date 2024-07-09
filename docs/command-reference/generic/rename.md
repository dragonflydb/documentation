---
description: "Learn Redis RENAME command which renames a key."
---

import PageTitle from '@site/src/components/PageTitle';

# RENAME

<PageTitle title="Redis RENAME Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `RENAME` command in Redis is used to change the name of an existing key to a new name. This is particularly useful for refactoring data models, renaming keys based on changing business logic, or simply reorganizing your data structure without losing any data.

## Syntax

```cli
RENAME oldkey newkey
```

## Parameter Explanations

- **oldkey**: The current name of the key you want to rename.
- **newkey**: The new name for the key. If `newkey` already exists, it will be overwritten.

## Return Values

- **OK**: The command returns "OK" if the key was renamed successfully.
- **Error**: An error is returned if:
  - `oldkey` does not exist.
  - `oldkey` and `newkey` are the same.

## Code Examples

```cli
dragonfly> SET mykey "value"
OK
dragonfly> RENAME mykey newkey
OK
dragonfly> GET newkey
"value"
dragonfly> GET mykey
(nil)
```

## Best Practices

- Ensure that `newkey` is not inadvertently overwriting critical data. This can be managed by using the `RENAMENX` command which only renames if the new key does not exist.
- Use descriptive and meaningful key names to avoid unnecessary renaming operations.

## Common Mistakes

- Attempting to rename a key that does not exist will result in an error.
- Renaming a key to the same name (i.e., `RENAME oldkey oldkey`) will result in an error.

## FAQs

### What happens if the `newkey` already exists?

If `newkey` already exists, it will be overwritten with the value of `oldkey`.

### Can I rename a key to itself?

No, Redis will return an error if you try to rename a key to itself.
