---
description: "Understand the use of Redis UNLINK command to delete keys avoiding blocking operations."
---

import PageTitle from '@site/src/components/PageTitle';

# UNLINK

<PageTitle title="Redis UNLINK Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `UNLINK` command in Redis is used to delete one or more keys. Unlike the traditional `DEL` command, `UNLINK` is non-blocking: it runs in constant time by delegating the actual removal of the keys to a background thread. This makes it particularly useful in scenarios where you need to delete large datasets without impacting the performance of your Redis server.

## Syntax

```cli
UNLINK key [key ...]
```

## Parameter Explanations

- **key**: The name of the key to be removed. You can specify multiple keys in a single `UNLINK` command. If a key does not exist, it is ignored.

## Return Values

The `UNLINK` command returns an integer representing the number of keys that were successfully unlinked.

### Example Outputs

- (integer) 1 — One key was successfully unlinked.
- (integer) 0 — No keys were unlinked, possibly because they did not exist.

## Code Examples

```cli
dragonfly> SET mykey "value"
OK
dragonfly> UNLINK mykey
(integer) 1
dragonfly> EXISTS mykey
(integer) 0
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> UNLINK key1 key2 key3
(integer) 2
```

## Best Practices

- Use `UNLINK` instead of `DEL` for deleting large keys or multiple keys to avoid blocking the Redis event loop.
- Regularly monitor and clean up keys that are no longer needed to optimize memory usage.

## Common Mistakes

- Attempting to `UNLINK` keys that do not exist will not generate an error but will count as non-unlinked keys in the return value.
- Misunderstanding that `UNLINK` immediately frees memory. The memory cleanup happens asynchronously, which can lead to temporary memory spikes if large datasets are unlinked frequently.

## FAQs

### What is the difference between `DEL` and `UNLINK`?

`DEL` is a blocking command that deletes keys in a synchronous manner, whereas `UNLINK` is non-blocking and delegates the deletion process to a background thread for faster performance.

### Can `UNLINK` be used with any type of key?

Yes, `UNLINK` can be used with any type of key including strings, lists, sets, hashes, and more.
