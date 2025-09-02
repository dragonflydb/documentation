---
description:  Learn how to use Redis COMMAND INFO to get details for a specific command.
---

import PageTitle from '@site/src/components/PageTitle';

# COMMAND INFO

<PageTitle title="Redis COMMAND INFO Command (Documentation) | Dragonfly" />

## Syntax

    COMMAND INFO command-name

**Time complexity:** O(1)

**ACL categories:** @slow, @connection

Returns information about a specific Dragonfly command.

This is a focused variant of `COMMAND` that returns details for a single command name.

The reply format matches one entry of the `COMMAND` output:

1. Name
2. Arity
3. Flags
4. First key
5. Last key
6. Step
7. ACL categories

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a single-element nested array describing the command, or a [null reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#nulls) if the command does not exist.

## Examples

```shell
dragonfly> COMMAND INFO GET
1) 1) GET
   2) (integer) 2
   3) 1) readonly
      2) fast
   4) (integer) 1
   5) (integer) 1
   6) (integer) 1
   7) 1) @READ
      2) @STRING
      3) @FAST
```

```shell
dragonfly> COMMAND INFO UNKNOWN_COMMAND
(nil)
```

## Tips

- Command names are case-insensitive.
- The reply includes ACL categories as the 7th element. See [`COMMAND`](./command.md) for category semantics and the general reply format.
- The output schema is stable but may include more fields in future versions.


## See also

[`COMMAND`](./command.md) | [`COMMAND COUNT`](./command-count.md) | [`ACL CAT`](../acl/cat.md)
