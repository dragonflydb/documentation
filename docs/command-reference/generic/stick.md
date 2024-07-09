---
description: "Learn to apply STICK command to prevent items from being evicted."
---

import PageTitle from '@site/src/components/PageTitle';

# STICK

<PageTitle title="Dragonfly STICK Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `STICK` command in Redis is used to manage key eviction policies, specifically ensuring that certain keys are "sticky" and do not get evicted. This is particularly useful in scenarios where specific keys must always remain in memory, such as configuration settings or critical data that should never be removed due to memory pressure.

## Syntax

```plaintext
STICK key
```

## Parameter Explanations

- `key`: The name of the key you want to make sticky. A sticky key will not be evicted from memory regardless of the eviction policy set on the Redis instance.

## Return Values

The `STICK` command returns an integer:

- `1` if the key was successfully marked as sticky.
- `0` if the key does not exist or could not be marked as sticky.

## Code Examples

```cli
dragonfly> SET mykey "important_value"
OK
dragonfly> STICK mykey
(integer) 1
dragonfly> STICK non_existent_key
(integer) 0
```

## Best Practices

- Use `STICK` sparingly to avoid overloading your memory with too many non-evictable keys.
- Combine `STICK` with appropriate monitoring to ensure critical keys remain available without exhausting memory resources.

## Common Mistakes

- Marking too many keys as sticky can lead to memory exhaustion since these keys cannot be evicted even under pressure.
- Using `STICK` on non-existent keys results in no changes and a return value of `0`.

## FAQs

### What happens if I mark too many keys as sticky?

If too many keys are marked as sticky, Redis may run out of memory since these keys won't be evicted even when memory limits are reached. This could potentially lead to performance issues or crashes if the system exhausts its available memory.

### Can I unstick a key?

Redis currently doesn't provide a direct command to "unstick" a key. You would need to manually delete the key and recreate it without using the `STICK` command.

### Does the `STICK` command affect all eviction policies?

Yes, keys marked as sticky are exempt from all types of eviction policies configured in Redis, making them persist in memory regardless of the overall eviction strategy.
