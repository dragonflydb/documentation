---
description: Learn how to use Redis FLUSHALL command to delete all keys in every database.
---

import PageTitle from '@site/src/components/PageTitle';

# FLUSHALL

<PageTitle title="Redis FLUSHALL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `FLUSHALL` command in Redis is used to remove all keys from all databases. It is particularly useful during development or testing when you need to quickly reset the state of your Redis server. This command is also helpful for clearing caches or when decommissioning a Redis instance.

## Syntax

```cli
FLUSHALL [ASYNC]
```

## Parameter Explanations

- `ASYNC`: Optional parameter that, if specified, will perform the flush operation asynchronously. This means the command will return immediately, and the actual deletion of keys will happen in the background.

## Return Values

The `FLUSHALL` command returns a simple string reply:

- `"OK"`: If the operation was successful.

## Code Examples

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> DBSIZE
(integer) 2
dragonfly> FLUSHALL
OK
dragonfly> DBSIZE
(integer) 0
dragonfly> SET key3 "value3"
OK
dragonfly> SET key4 "value4"
OK
dragonfly> FLUSHALL ASYNC
OK
```

## Best Practices

While using `FLUSHALL`, especially in production environments, ensure that it won't disrupt your application's operations. Consider using it during maintenance windows or with the `ASYNC` option to minimize impact.

## Common Mistakes

- **Accidental Execution**: Using `FLUSHALL` on a live environment can lead to complete data loss. Always double-check the command before executing.
- **Not Using ASYNC Properly**: Without `ASYNC`, large datasets might cause significant delays and block Redis operations until completion.

## FAQs

### Does `FLUSHALL` delete keys from all databases?

Yes, `FLUSHALL` removes all keys from all databases in the Redis instance.

### How does `FLUSHALL ASYNC` improve performance?

The `ASYNC` option allows the server to handle the flush command in the background, letting your application continue its operations without waiting for the command to complete.
