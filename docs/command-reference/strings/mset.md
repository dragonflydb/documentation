---
description: Learn the proper use of Redis MSET to set multiple keys to multiple values simultaneously.
---

import PageTitle from '@site/src/components/PageTitle';

# MSET

<PageTitle title="Redis MSET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MSET` command in Redis is used to set multiple key-value pairs in a single atomic operation. This command is particularly useful when you need to update several keys at once, ensuring that either all keys are updated or none are if an error occurs.

## Syntax

```plaintext
MSET key1 value1 [key2 value2 ...]
```

## Parameter Explanations

- **key1, key2, ...**: The keys that you want to set.
- **value1, value2, ...**: The values corresponding to each key.

Each key must have a corresponding value and vice versa.

## Return Values

`MSET` always returns `OK` since it will not raise any errors if provided with the correct number of arguments.

## Code Examples

```cli
dragonfly> MSET key1 "value1" key2 "value2" key3 "value3"
"OK"
dragonfly> GET key1
"value1"
dragonfly> GET key2
"value2"
dragonfly> GET key3
"value3"
```

## Best Practices

- Ensure you provide an even number of arguments to `MSET` for proper key-value pairing.
- Use `MSET` when multiple key updates are required simultaneously to maintain atomicity.

## Common Mistakes

- Providing an odd number of arguments will result in a syntax error since every key needs a corresponding value.

## FAQs

### What happens if one of the keys already exists?

`MSET` will overwrite the existing keys with the new values provided.

### Is `MSET` an atomic operation?

Yes, `MSET` is atomic. All specified keys are set at once, ensuring consistency.
