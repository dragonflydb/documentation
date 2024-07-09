---
description: "Master Redis DISCARD command that discards all commands issued after MULTI."
---

import PageTitle from '@site/src/components/PageTitle';

# DISCARD

<PageTitle title="Redis DISCARD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `DISCARD` command in Redis is used to cancel a transaction started with `MULTI`. This command discards all the commands issued after the `MULTI` command and before the `EXEC` command. It is useful when you want to abort a transaction due to some conditional logic or error encountered during the transaction's preparation.

## Syntax

```plaintext
DISCARD
```

## Parameter Explanations

This command does not take any parameters.

## Return Values

- **OK**: If the transaction was successfully discarded.
- **Error**: If `DISCARD` is called outside of a `MULTI`/`EXEC` context.

## Code Examples

```cli
dragonfly> MULTI
OK
dragonfly> SET key1 "value1"
QUEUED
dragonfly> SET key2 "value2"
QUEUED
dragonfly> DISCARD
OK
dragonfly> GET key1
(nil)
dragonfly> GET key2
(nil)
```

## Best Practices

- Use `DISCARD` only when necessary to ensure that transactions are managed appropriately.
- Ensure that your application logic can handle cases where a transaction needs to be aborted.

## Common Mistakes

- Attempting to use `DISCARD` outside of a `MULTI`/`EXEC` block will result in an error.
- Forgetting to handle the state after a `DISCARD`, leaving the system in an unintended state.

## FAQs

### What happens if I issue commands after `DISCARD`?

After issuing `DISCARD`, the transaction context is cleared, so subsequent commands are executed immediately rather than being queued for the transaction.

### Can `DISCARD` be used inside Lua scripts?

No, `DISCARD` cannot be called from within Lua scripts. Lua scripts are atomic by nature and do not require transactional control via `MULTI`/`DISCARD`.
