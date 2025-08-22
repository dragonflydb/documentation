---
description: Simulate execution of a command from a user
---

import PageTitle from '@site/src/components/PageTitle';

# ACL GENPASS

<PageTitle title="Redis ACL GENPASS Command (Documentation) | Dragonfly" />

## Syntax

    ACL GENPASS [bits]

**ACL categories:** @slow

This command is a password generator that polls from `/dev/urandom` if available.
Otherwise, it uses a weaker system.

The command returns a hexadecimal representation of a binary string.
By default it emits 256 bits (so 64 hex characters), which is tunable via the command argument `bits`.
Note that the number of bits provided is rounded to the next multiple of 4.

## Return

- [Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec#bulk-strings): pseudorandom data.
  By default it contains 64 bytes, representing 256 bits of data.
  If the `bits` argument was given, the output string length is the number of specified bits (rounded to the next multiple of 4) divided by 4.

## Examples

```shell
dragonfly> ACL GENPASS 3
"a"
dragonfly> ACL GENPASS 32
"69ee5ab3"
dragonfly> ACL GENPASS
"3aa763f86ced2b83b4cd6a4d83f17cb75e73b4e0d9f8655411faef9ff2c8fd8f"
```
