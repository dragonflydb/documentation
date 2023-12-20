---
description: "Learn how to use Redis ACL SETUSER to modify or create new user rules in the Access Control List."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL SETUSER

<PageTitle title="Redis ACL SETUSER Command (Documentation) | Dragonfly" />

## Syntax

    ACL SETUSER username [rule [rule ...]]

**ACL categories:** @admin, @slow, @dangerous

## ACL Rules

Dragonfly ACL rules are split into two categories:

- [Command Rules](#command-rules) that define command permissions.
- [User Management Rules](#user-management-rules) that define the user state.

### Command Rules

- `+@<category>`: Grants all the commands in the specified category to the list of commands the user is able to execute. For example, `+@string` adds all the string commands.
- `-@<category>`: Like `+@<category>` but removes all the commands in the category instead of adding them.
- `+ALL`: Grants all the available groups to the user.
- `-ALL`: Revokes all the available groups from the user.

### User Management Rules

- `ON`: Set the user as active, it will be possible to authenticate as this user using `AUTH <username> <password>`.
- `OFF`: Set user as not active, it will be impossible to authenticate as this user.
- `>password`: Set or update the password of this user.
- `nopass`: Allow the user to authenticate with `any` password.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` on success. If the rules contain errors, the error is returned.

## Examples

```shell
dragonfly> ACL SETUSER myuser ON >mypass +@string +@fast -@slow ~*
OK
```
