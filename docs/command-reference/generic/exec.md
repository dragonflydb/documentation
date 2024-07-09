---
description: "Discover how to use Redis EXEC command to execute all commands issued after MULTI."
---

import PageTitle from '@site/src/components/PageTitle';

# EXEC

<PageTitle title="Redis EXEC Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`EXEC` is a crucial Redis command used within the context of transactions. It executes all previously queued commands in a transaction block initiated by `MULTI`. This ensures atomicity, where either all commands are executed or none if an error occurs. Typical use cases include batch updates, ensuring data consistency, and handling operations that must be performed together.

## Syntax

```plaintext
EXEC
```

## Parameter Explanations

`EXEC` does not take any parameters. It simply executes all commands that have been queued after a `MULTI` command.

## Return Values

- If the transaction executes successfully, `EXEC` returns an array of the results for each of the commands executed within the transaction.
- If the transaction fails, it returns a `null` reply to indicate that the transaction was discarded.

Example output:

```plaintext
1) (integer) 1
2) "OK"
3) "value"
```

## Code Examples

```cli
dragonfly> MULTI
OK
dragonfly> SET key1 "value1"
QUEUED
dragonfly> INCR counter
QUEUED
dragonfly> GET key1
QUEUED
dragonfly> EXEC
1) OK
2) (integer) 1
3) "value1"
```

## Best Practices

- Always ensure that `MULTI` and `EXEC` encapsulate the commands that need to be executed atomically.
- Handle possible `null` replies from `EXEC`, which indicate that the transaction has been discarded due to errors.

## Common Mistakes

- Forgetting to issue the `EXEC` command after `MULTI`, leaving the transaction unexecuted.
- Misinterpreting the QUEUED responses as actual execution results; they merely indicate that the commands have been added to the transaction queue.

## FAQs

### What happens if one of the commands in the transaction fails?

If a command in the transaction queue fails (syntax error, wrong type operation, etc.), `EXEC` will return a `null` reply, and none of the queued commands will be executed.

### Can I nest MULTI/EXEC blocks?

No, nested MULTI/EXEC blocks are not supported. Attempting to use `MULTI` inside an already-existing transaction will result in an error.

### How do I cancel a transaction?

You can cancel a transaction by issuing the `DISCARD` command before calling `EXEC`.
