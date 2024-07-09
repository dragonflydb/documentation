---
description: Print the ACL logs
---

import PageTitle from '@site/src/components/PageTitle';

# ACL LOG

<PageTitle title="Redis ACL LOG Command (Documentation) | Dragonfly" />

## Syntax

    ACL LOG [count | RESET]

**ACL categories:** @admin, @slow, @dangerous

The command shows a list of recent ACL security events:

1. Failures to authenticate their connections with AUTH or HELLO.
2. Commands denied because against the current ACL rules.

By default ten entries are returned unless `COUNT` is specified.

The `RESET` arguments clears the log.

## Return

When called to show security events:

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of ACL security events.

When called with `RESET`:
[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` if the security log was cleared.

## Examples

```shell
dragonfly> ACL LOG
1)  1) reason
    2) AUTH
    3) object
    4) AUTH
    5) username
    6) mike
    7) age-seconds
    8) 2.465420372
    9) client-info
   10) id=6 addr=127.0.0.1:40390 laddr=127.0.0.1:6379 fd=24 name= irqmatch=0 age=9 idle=0 phase=process db=0 qbuf=0 qbuf-free=0 obl=0 argv-mem=0 oll=0 omem=0 tot-mem=0 multi=0 psub=0 sub=0
   11) timestamp-created
   12) (integer) 1697469722374275368
```
