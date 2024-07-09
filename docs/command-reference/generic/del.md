---
description: "Learn how to use Redis DEL command to delete a key."
---

import PageTitle from '@site/src/components/PageTitle';

# DEL

<PageTitle title="Redis DEL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `DEL` command in Redis is used to delete one or more keys. It is commonly used to free up memory space by removing unnecessary data, clear expired keys manually, or reset states of certain keys.

## Syntax

```
DEL key [key ...]
```

## Parameter Explanations

- `key`: The name of the key(s) to be deleted. Multiple keys can be specified, separated by spaces.

## Return Values

The command returns an integer representing the number of keys that were removed.

### Example Returns:

- If one key is deleted: `(integer) 1`
- If no keys are found for deletion: `(integer) 0`
- If multiple keys are deleted: `(integer) N` (where N is the number of keys deleted)

## Code Examples

```cli
dragonfly> SET mykey "value"
OK
dragonfly> DEL mykey
(integer) 1
dragonfly> DEL non_existing_key
(integer) 0
dragonfly> MSET key1 "value1" key2 "value2" key3 "value3"
OK
dragonfly> DEL key1 key2 key3
(integer) 3
```

## Best Practices

- Use the `EXPIRE` command to set a time-to-live (TTL) for keys that should be automatically deleted after a certain period instead of relying solely on manual deletion with `DEL`.

## Common Mistakes

- Deleting non-existing keys will not cause an error but will return 0, indicating that no keys were removed.

## FAQs

### What happens if I try to delete a key that doesn’t exist?

The `DEL` command will return `(integer) 0`, indicating that no keys were removed.

### Can I delete multiple keys at once?

Yes, you can specify multiple keys in a single `DEL` command, and it will return the number of keys successfully deleted.

### Is there any difference between deleting a large number of keys individually and using a single DEL command?

Using a single `DEL` command to delete multiple keys is more efficient than issuing multiple individual `DEL` commands due to reduced round-trip time (RTT).
