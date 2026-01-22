---
description: Learn how to use Redis DELEX command for conditional key deletion.
---

import PageTitle from '@site/src/components/PageTitle';

# DELEX

<PageTitle title="Redis DELEX Command (Documentation) | Dragonfly" />

## Introduction

The `DELEX` command provides conditional key deletion based on value or digest comparison.
It enables atomic conditional operations, allowing you to delete keys only when specific conditions are met.
This is useful for implementing optimistic locking patterns and ensuring data consistency.

## Syntax

```shell
DELEX key [IFEQ value | IFNE value | IFDEQ digest | IFDNE digest]
```

**Time complexity:**
- O(1) when no condition is specified
- O(min(M,N)) for value comparisons (IFEQ/IFNE) where M and N are value lengths
- O(N) for digest comparisons (IFDEQ/IFDNE) where N is the length of the stored string value

**ACL categories:** @keyspace, @write, @fast

## Parameter Explanations

- `key`: The key to conditionally delete. Must be a string type for conditional operations.
- `IFEQ value` (optional): Delete the key only if its value matches the provided value.
- `IFNE value` (optional): Delete the key only if its value differs from the provided value.
- `IFDEQ digest` (optional): Delete the key only if its digest matches the provided digest (16-character hex string).
- `IFDNE digest` (optional): Delete the key only if its digest differs from the provided digest (16-character hex string).

## Return Values

- Returns `1` if the key was deleted.
- Returns `0` if the key was not deleted (condition not met or key doesn't exist).

## Code Examples

### Basic DELEX Without Condition

Without a condition, `DELEX` behaves like the standard [`DEL`](./del.md) command:

```shell
dragonfly$> SET mykey "hello"
OK
dragonfly$> DELEX mykey
(integer) 1
dragonfly$> EXISTS mykey
(integer) 0
```

### DELEX with IFEQ (Delete If Equal)

Delete the key only if the value matches:

```shell
dragonfly$> SET mykey "hello"
OK
dragonfly$> DELEX mykey IFEQ "hello"
(integer) 1

dragonfly$> SET mykey "hello"
OK
dragonfly$> DELEX mykey IFEQ "world"
(integer) 0
dragonfly$> GET mykey
"hello"
```

### DELEX with IFNE (Delete If Not Equal)

Delete the key only if the value differs:

```shell
dragonfly$> SET mykey "hello"
OK
dragonfly$> DELEX mykey IFNE "world"
(integer) 1

dragonfly$> SET mykey "hello"
OK
dragonfly$> DELEX mykey IFNE "hello"
(integer) 0
dragonfly$> GET mykey
"hello"
```

### DELEX with IFDEQ (Delete If Digest Equal)

Delete the key only if the digest matches:

```shell
dragonfly$> SET mykey "test"
OK
dragonfly$> DIGEST mykey
"a1b2c3d4e5f67890"
dragonfly$> DELEX mykey IFDEQ "a1b2c3d4e5f67890"
(integer) 1

dragonfly$> SET mykey "test"
OK
dragonfly$> DELEX mykey IFDEQ "0000000000000000"
(integer) 0
dragonfly$> GET mykey
"test"
```

### DELEX with IFDNE (Delete If Digest Not Equal)

Delete the key only if the digest differs:

```shell
dragonfly$> SET mykey "test"
OK
dragonfly$> DIGEST mykey
"a1b2c3d4e5f67890"
dragonfly$> DELEX mykey IFDNE "0000000000000000"
(integer) 1

dragonfly$> SET mykey "test"
OK
dragonfly$> DELEX mykey IFDNE "a1b2c3d4e5f67890"
(integer) 0
dragonfly$> GET mykey
"test"
```

### Optimistic Locking Pattern

Use `DELEX` for optimistic locking to ensure data hasn't changed:

```shell
dragonfly$> SET counter "100"
OK
dragonfly$> DIGEST counter
"d4f3c8b2a1e6f7d9"

# Later, delete only if the value hasn't changed
dragonfly$> DELEX counter IFDEQ "d4f3c8b2a1e6f7d9"
(integer) 1
```

## Best Practices

- Use `DELEX` with digest comparisons (`IFDEQ`/`IFDNE`) for efficient optimistic locking without transferring full values.
- Use value comparisons (`IFEQ`/`IFNE`) when you need exact value matching.
- Always check the return value to determine if the deletion was successful.
- For optimistic locking, compute the digest first with [`DIGEST`](../strings/digest.md), then use `DELEX IFDEQ` to ensure atomicity.

## Common Mistakes

- Providing only a condition without a value/digest (e.g., `DELEX key IFEQ`) will result in a syntax error.
- Using `DELEX` with conditional options on non-string keys will result in a `WRONGTYPE` error.
- Forgetting that `DELEX` returns `0` when the condition is not met, not an error.

## FAQs

### What happens if the key doesn't exist?

If the key doesn't exist, `DELEX` returns `0` regardless of the condition specified.

### Can DELEX be used with non-string values?

For basic `DELEX key` without conditions, yes. However, conditional operations (IFEQ, IFNE, IFDEQ, IFDNE) only work with string values.

### Is DELEX atomic?

Yes, `DELEX` is atomic. The check and delete operation happens as a single atomic operation within Dragonfly's transaction framework.

### Is DELEX replicated?

Yes, `DELEX` operations are journaled and replicated to replicas, ensuring consistency across your cluster.

### How is DELEX different from DEL?

`DELEX` extends [`DEL`](./del.md) by adding conditional deletion based on value or digest matching. Without conditions, `DELEX key` behaves identically to `DEL key`.

### Is DELEX compatible with Redis?

Yes, `DELEX` is compatible with Redis 8.4.0 and later versions.
