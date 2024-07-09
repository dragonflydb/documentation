---
description: "Discover the Redis MULTI command used for transactions."
---

import PageTitle from '@site/src/components/PageTitle';

# MULTI

<PageTitle title="Redis MULTI Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MULTI` command in Redis is used to start a transaction. Transactions allow multiple commands to be executed sequentially as a single isolated operation. This ensures that either all commands are executed or none are, thus maintaining consistency. Typical scenarios for using `MULTI` include batch updates, atomic operations on multiple keys, and ensuring data integrity during complex state changes.

## Syntax

```cli
MULTI
```

## Parameter Explanations

The `MULTI` command does not take any parameters. It simply initiates a transaction block. Commands issued after `MULTI` will be queued until an `EXEC` or `DISCARD` command is received.

## Return Values

Upon issuing the `MULTI` command, Redis responds with:

```cli
OK
```

This indicates that the transaction block has started successfully. Subsequent commands will be queued and not executed immediately until `EXEC` or `DISCARD` is called.

## Code Examples

```cli
dragonfly> MULTI
OK
dragonfly> SET key1 "value1"
QUEUED
dragonfly> INCR key2
QUEUED
dragonfly> EXEC
1) OK
2) (integer) 1
```

In this example:

- `MULTI` starts the transaction.
- `SET key1 "value1"` and `INCR key2` are queued.
- `EXEC` executes all queued commands atomically.

If the transaction needs to be aborted:

```cli
dragonfly> MULTI
OK
dragonfly> SET key1 "newValue"
QUEUED
dragonfly> DISCARD
OK
```

Here, the `DISCARD` command cancels the transaction, and no queued commands are executed.

## Best Practices

- Always ensure that the commands within a transaction block (`MULTI`...`EXEC`) do not depend on results from each other unless using `WATCH`.
- Minimize the number of commands in a transaction to reduce the time the Redis server holds the lock, which can improve performance.

## Common Mistakes

### Forgetting to Call `EXEC` or `DISCARD`

Forgetting to call `EXEC` or `DISCARD` will leave the transaction open, which can lead to unexpected behavior as Redis will continue to queue commands.

## FAQs

### What happens if one command in a transaction fails?

All commands within a transaction are executed sequentially. If one command fails, the transaction will still execute the remaining commands unless it fails due to a syntax error. However, failed commands will return their respective error responses.

### Can transactions be nested in Redis?

No, transactions cannot be nested. Issuing `MULTI` within a transaction block will result in an error.

### How can I handle conditional execution in Redis transactions?

You can use the `WATCH` command to monitor specific keys and conditionally execute a transaction using `MULTI`...`EXEC` based on the monitored keys' states.
