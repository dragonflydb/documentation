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

Dragonfly ACL rules are split into four categories:

- [Command Rules](#command-rules) that define command permissions.
- [Key Permissions](#key-permissions) that define keyspace permissions.
- [Pub/Sub Permissions](#pubsub-permissions) that define pub/sub permissions.
- [User Management Rules](#user-management-rules) that define the user state.

### Command Rules

- `+@<category>`: Grants all the commands in the specified category to the list of commands the user is able to execute. For example, `+@string` adds all the string commands.
- `-@<category>`: Like `+@<category>` but removes all the commands in the category instead of adding them.
- `+@ALL`: Grants all the available groups to the user.
- `-@ALL`: Revokes all the available groups from the user.

### Key Permissions

Glob-style pattern that controls access to keys.

- `~<pattern>`: Allows the user to access the keys specified by the `<pattern>`. For example, `~foo` or `~f*o`.
- `%R~<pattern>`: Allows the user to only **read** the keys specified by the `<pattern>`.
- `%W~<pattern>`: Allows the user to only **write** the keys specified by the `<pattern>`.
- `%RW~<pattern>`: Alias for `~<pattern>`.
- `allkeys`: Alias for `~*`.
- `resetkeys`: Revokes access to all keys. The user can't access any key.

### Pub/Sub Permissions

Glob-style pattern that controls access to pub/sub channels.

- `&*`: Grants access to all pub/sub channels.
- `&<pattern>`: Grants access to channels with names specified by the `<pattern>`.
- `resetchannels`: Revokes access to all channels. The user can't access, publish, or subscribe to any channel.
- `allchannels`: Alias for `&*`.

**Note:** For all command variants that start with `P` (like `PSUBSCRIBE`), the match must be a literal match.
For example, if a user's ACL contains the pattern `&fo&` and the user tries to `PPSUBSRIBE foo`, it would fail.
However, if the user's ACL contains the pattern `&foo` instead, it would pass.
This restriction does not exist on the rest of the family of pub/sub commands.

### User Management Rules

- `ON`: Set the user as active, it will be possible to authenticate as this user using `AUTH <username> <password>`.
- `OFF`: Set user as not active, it will be impossible to authenticate as this user.
- `>password`: Set or update the list of passwords for this user.
- `nopass`: Allow the user to authenticate with `any` password.

### Database Selectors

Dragonfly ACL supports **database selectors**, a Dragonfly-specific feature that allows you to restrict user access to specific logical databases. This provides fine-grained control over which databases authenticated users can access. See database-selectors for more.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` on success. If the rules contain errors, the error is returned.

## Examples

```shell
dragonfly> ACL SETUSER myuser ON >mypass >mysecondpass ~my*key &chan*el +@string +@fast -@slow ~*
OK
```
