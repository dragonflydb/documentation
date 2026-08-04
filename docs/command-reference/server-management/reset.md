---
description: Learn how to use Redis RESET to clear connection-scoped state in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# RESET

<PageTitle title="Redis RESET Command (Documentation) | Dragonfly" />

## Syntax

    RESET

**Time complexity:** O(1)

**ACL categories:** @fast, @connection

Clears connection-scoped state without closing the connection. Dragonfly:

- Aborts an active `MULTI` transaction and unwatches all keys.
- Removes channel and pattern Pub/Sub subscriptions.
- Exits `MONITOR` mode.
- Disables `CLIENT TRACKING`.
- Selects database 0.
- Switches the connection back to RESP2.
- Restores the default ACL identity and clears authentication.

If authentication is required, the client must call `AUTH` again after
`RESET`. The command changes only connection state; it does not delete data.

:::note Dragonfly v1.40 compatibility

Dragonfly preserves the name set with `CLIENT SETNAME` when the connection is
reset. Valkey clears the client name.

:::

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings):
`RESET`.

## Examples

Abort a transaction without closing the connection:

```shell
dragonfly> MULTI
OK
dragonfly> SET key value
QUEUED
dragonfly> RESET
RESET
dragonfly> EXEC
(error) ERR EXEC without MULTI
```

`RESET` selects database 0 but does not delete data from the previously
selected database:

```shell
dragonfly> SELECT 1
OK
dragonfly> SET reset:key value
OK
dragonfly> RESET
RESET
dragonfly> GET reset:key
(nil)
dragonfly> SELECT 1
OK
dragonfly> GET reset:key
"value"
```

## See also

[`AUTH`](./auth.md) | [`SELECT`](./select.md) | [`QUIT`](./quit.md)
