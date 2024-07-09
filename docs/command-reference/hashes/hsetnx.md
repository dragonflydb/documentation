---
description: "Learn how to use Redis HSETNX command to set the value of a hash field, only if the field does not exist. Perfect for unique data entries."
---

import PageTitle from '@site/src/components/PageTitle';

# HSETNX

<PageTitle title="Redis HSETNX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`HSETNX` is a Redis command used to set the value of a field in a hash only if the field does not already exist. This is useful for ensuring that certain fields are set only once, preventing accidental overwrites.

## Syntax

```cli
HSETNX key field value
```

## Parameter Explanations

- **key**: The name of the hash.
- **field**: The specific field in the hash.
- **value**: The value to set if the field does not already exist.

## Return Values

- `(integer) 1`: Indicates that the field was set successfully because it did not previously exist.
- `(integer) 0`: Indicates that the field was not set because it already exists.

## Code Examples

```cli
dragonfly> HSETNX myhash field1 "value1"
(integer) 1
dragonfly> HSETNX myhash field1 "value2"
(integer) 0
dragonfly> HGET myhash field1
"value1"
```

## Best Practices

- Ensure that `HSETNX` is used when setting initial values that should not be overwritten.
- Combine with other commands like `HEXISTS` to check if a field exists before attempting further operations.

## Common Mistakes

- Using `HSETNX` without understanding that it will not overwrite existing fields. This can lead to unexpected behavior if you assume the field will always be updated.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `HSETNX` will create a new hash with the specified field and value.

### Can `HSETNX` be used to update an existing field?

No, `HSETNX` will not update an existing field; it only sets the field if it does not already exist.
