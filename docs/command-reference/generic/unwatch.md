---
description: "Learn to use Redis UNWATCH command that flushes all previously watched keys."
---

import PageTitle from '@site/src/components/PageTitle';

# UNWATCH

<PageTitle title="Redis UNWATCH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `UNWATCH` command in Redis is used to cancel the effects of all previous `WATCH` commands. This is essential in situations where you have watched one or more keys using `WATCH` to monitor their changes for conditional transactions (`MULTI`/`EXEC`), but need to abandon the watch due to conditional logic, error handling, or any other reason before executing the transaction.

## Syntax

```plaintext
UNWATCH
```

## Parameter Explanations

The `UNWATCH` command does not take any parameters. It is a standalone command that simply cancels all watched keys.

## Return Values

The `UNWATCH` command returns a simple string reply:

- `OK`: Indicates that all watched keys have been successfully unwatched.

Example:

```cli
dragonfly> UNWATCH
"OK"
```

## Code Examples

Using the Redis CLI with Dragonfly:

```cli
dragonfly> WATCH mykey
"OK"
dragonfly> SET mykey "value1"
"OK"
dragonfly> UNWATCH
"OK"
dragonfly> GET mykey
"value1"
```

In this example, after watching `mykey`, we set a value and then decide to unwatch it. The `UNWATCH` command ensures that no keys are being watched anymore.

## Best Practices

- Use `UNWATCH` when you encounter an error or change in logic that means you should not proceed with your transaction. This helps to clean up any state that may interfere with future operations.
- Always consider using `UNWATCH` in your exception handling code blocks to avoid accidental retention of key watches.

## Common Mistakes

- Forgetting to `UNWATCH` if your conditional logic decides not to execute a transaction can lead to unexpected behaviors in subsequent operations where those keys might still be watched.

## FAQs

### What happens if I call `UNWATCH` without any prior `WATCH` commands?

Calling `UNWATCH` without any prior `WATCH` commands has no additional effect; it simply returns `OK`.

### Can `UNWATCH` be used inside a transaction?

No, `UNWATCH` must be called outside a transaction. Once inside a transaction block (between `MULTI` and `EXEC`), you cannot issue `UNWATCH`.
