---
description: "Learn how to use Redis ACL DELUSER to remove specified users from the Access Control List and enhance database security."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL DELUSER

<PageTitle title="Redis ACL DELUSER Command (Documentation) | Dragonfly" />

## Syntax

    ACL DELUSER username

**ACL categories:** @admin, @slow, @dangerous

Delete a user from the ACL registry. If the user has open connections, those connections will be killed.
Keep in mind that if the user is in the middle of a running script or if any other transactions from that user have started,
the connection will close and the transaction will complete normally (unless there was an error).
This is a deterministic behavior since, by the time the user was deleted from the system,
the user had already begun (and consequently had the credentials) to start and complete that transaction.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` if the user was deleted, error otherwise.

## Examples

```shell
dragonfly> ACL DELUSER myuser
(error) ERR User myuser does not exist

dragonfly> ACL SETUSER myuser ON >mypass +@string +@fast -@slow
OK

dragonfly> ACL DELUSER myuser
OK
```
