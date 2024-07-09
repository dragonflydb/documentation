---
description: "Learn how the Redis TOUCH command alters the last access time of a key."
---

import PageTitle from '@site/src/components/PageTitle';

# TOUCH

<PageTitle title="Redis TOUCH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `TOUCH` command in Redis is used to update the last access time of one or more keys without altering their values. This can be useful for cache management, where you need to keep certain keys from expiring by marking them as recently used.

## Syntax

```plaintext
TOUCH key [key ...]
```

## Parameter Explanations

- **key**: The name of the key whose last access time you want to update. You can specify multiple keys.

## Return Values

The `TOUCH` command returns an integer indicating the number of keys that were successfully updated.

### Example:

If you run `TOUCH mykey1 mykey2` and both keys exist, the command might return:

```plaintext
(integer) 2
```

## Code Examples

```cli
dragonfly> SET mykey1 "value1"
OK
dragonfly> SET mykey2 "value2"
OK
dragonfly> TOUCH mykey1 mykey2
(integer) 2
dragonfly> TOUCH mykey3
(integer) 0
```

## Best Practices

- Use `TOUCH` to extend the life of frequently accessed keys in a cache without modifying their values.
- Monitor the number of keys updated using the return value to ensure your intended keys are being touched.

## Common Mistakes

- Using `TOUCH` on keys that don't exist will not result in an error but will return 0, indicating no keys were touched.
- Assuming `TOUCH` modifies the key's value, it only updates the last access time.

## FAQs

### Does the TOUCH command alter the TTL (Time to Live) of a key?

No, the `TOUCH` command only updates the last access time of the key; it does not change its TTL.

### Can I use TOUCH with expired keys?

No, `TOUCH` has no effect on expired keys since they are considered non-existent in Redis.
