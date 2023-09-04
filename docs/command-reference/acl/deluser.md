---
description: Delete a user
---

# ACL DELUSER

## Syntax

    ACL DELUSER username

**ACL categories:** @admin, @slow, @dangerous


Delete a user from the ACL registry. If the user has open connections, these will be killed. Keep in mind that if the user is in the middle of a running script or if any other transaction from that user has started, the connection will close and the transaction will complete normally(unless there was an error). This is a deterministic behaviour since by the time the user was deleted from the system, he had already begun (and consequently had the credentials) to start and complete that transaction.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `ok` if the user was deleted, error otherwise.


## Examples

```shell
dragonfly> ACL DELUSER myuser
"ok"
```
