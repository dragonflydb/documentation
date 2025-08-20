---
description: Simulate execution of a command from a user
---

import PageTitle from '@site/src/components/PageTitle';

# ACL DRYRUN

<PageTitle title="Redis ACL GENPASS Command (Documentation) | Dragonfly" />

## Syntax

    ACL GENPASS digits

**ACL categories:** @slow

The ACL GENPASS command is a password generator that polls from /dev/urandom if available(otherwise it uses a weaker system).

The command returns a hexadecimal representation of a binary string. By default it emits 256 bits (so 64 hex characters) which is tunable via the command argument. Note, that the number of bits provided is rounded to the next multiple of 4.

## Return

- [Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` on success.
- [Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): pseudorandom data. By default it contains 64 bytes, representing 256 bits of data. If bits was given, the output string length is the number of specified bits (rounded to the next multiple of 4) divided by 4.

## Examples

```shell
dragonfly> ACL GENPASS 3 
"ot2"
```
