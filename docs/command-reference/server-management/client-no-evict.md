---
description: Set client eviction mode for the current connection
---

# CLIENT NO-EVICT

## Syntax

    CLIENT NO-EVICT <ON | OFF>

**Time complexity:** O(1)

The `CLIENT NO-EVICT` command sets the [client eviction](https://redis.io/topics/clients#client-eviction) mode for the current connection.

When turned on and client eviction is configured, the current connection will be excluded from the client eviction process even if we're above the configured client eviction threshold.

When turned off, the current client will be re-included in the pool of potential clients to be evicted (and evicted if needed).

See [client eviction](https://redis.io/topics/clients#client-eviction) for more details.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK`.
