---
description: Get the time since a Redis object was last accessed
---

# OBJECT IDLETIME

## Syntax

    OBJECT IDLETIME key

**Time complexity:** O(1)

This command returns the time in seconds since the last access to the value stored at `<key>`.

The command is only available when the `maxmemory-policy` configuration directive is not set to one of the LFU policies.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers)

The idle time in seconds.