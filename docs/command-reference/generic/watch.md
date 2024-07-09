---
description: "Learn the use of Redis WATCH command to monitor keys for conditional transactions."
---

import PageTitle from '@site/src/components/PageTitle';

# WATCH

<PageTitle title="Redis WATCH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`WATCH` is a Redis command used to provide the functionality of optimistic locking in transactions. It monitors the specified keys and ensures that the transaction only executes if the watched keys remain unchanged. Typical scenarios include implementing counters, maintaining financial balances, or other state changes where consistency is paramount.

## Syntax

```plaintext
WATCH key [key ...]
```

## Parameter Explanations

- **key**: One or more keys to monitor for changes. If any of these keys are modified before the `EXEC` command, the entire transaction will be aborted.

## Return Values

- **OK**: If the keys were successfully watched.

Example:

```cli
dragonfly> WATCH mykey
OK
```

## Code Examples

```cli
dragonfly> SET mykey "initial"
OK
dragonfly> WATCH mykey
OK
dragonfly> MULTI
OK
dragonfly> SET mykey "updated"
QUEUED
dragonfly> EXEC
(nil)   # This indicates that the transaction was aborted because another client modified 'mykey' after the WATCH command.
```

In another session:

```cli
dragonfly> SET mykey "changed"
OK
```

Back to the first session:

```cli
dragonfly> EXEC
(nil)   # Transaction aborted due to change in 'mykey'
```

## Best Practices

- Use `WATCH` judiciously, as it can increase the complexity of your transaction logic.
- Combine `WATCH` with appropriate error handling to retry transactions when they are aborted.

## Common Mistakes

- Not handling the nil response from `EXEC`, which can lead to silent transaction failures.
- Watching too many keys, which increases the likelihood of transaction aborts.

## FAQs

### What happens if I issue a `UNWATCH` after `WATCH`?

`UNWATCH` will cancel all previously watched keys, ensuring the next `EXEC` will not be conditional based on those keys.

### Can I use `WATCH` outside of a MULTI/EXEC block?

Yes, but doing so won't have any effect since `WATCH` is designed to work within transactions.
