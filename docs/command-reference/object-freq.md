---
description: Get the logarithmic access frequency counter of a Redis object
---

# OBJECT FREQ

## Syntax

    OBJECT FREQ key

**Time complexity:** O(1)

This command returns the logarithmic access frequency counter of a Redis object stored at `<key>`.

The command is only available when the `maxmemory-policy` configuration directive is set to one of the LFU policies.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers)

The counter's value.