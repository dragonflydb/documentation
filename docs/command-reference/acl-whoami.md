---
description: Return the name of the user associated to the current connection
---

# ACL WHOAMI

## Syntax

    ACL WHOAMI 

**Time complexity:** O(1)

Return the username the current connection is authenticated with.
New connections are authenticated with the "default" user. They
can change user using `AUTH`.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the username of the current connection.

## Examples

```
> ACL WHOAMI
"default"
```
