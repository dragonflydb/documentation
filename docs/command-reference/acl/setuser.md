---
description: "Learn how to use Redis ACL SETUSER to modify or create new user rules in the Access Control List."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL SETUSER

<PageTitle title="Redis ACL SETUSER Command (Documentation) | Dragonfly" />

## Syntax

    ACL SETUSER username [rule [rule ...]]

**ACL categories:** @admin, @slow, @dangerous

Create an ACL user with the specified rules or modify the rules of an existing user.

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

### Database Selectors Rules

Dragonfly ACL supports **database selectors**, a Dragonfly-specific feature that allows you to restrict user access to
specific logical databases. This provides fine-grained control over which databases authenticated users can access.

- `$<database>`: Restricts the user to access only the specified database number.
  For example, `$0` restricts to database 0, `$1` to database 1, etc.
- `$all`: Allows the user to access all databases (default behavior).

#### Database Selector Behavior

- When a user is restricted to a specific database, they can only execute commands on that database.
- Attempting to `SELECT` a different database or access keys in a non-permitted database will result in an error.
- The database number must be less than the configured `--dbnum` value.
- By default, if no database selector is specified, users have access to all databases (`$all`).
- A connection that uses`AUTH` will automatically select the relevant logical database (no need to `AUTH` + `SELECT`).

#### Database Selector Use Cases

- **Multi-tenancy**: Isolate different tenants or applications by assigning each to a dedicated database.
- **Development environments**: Give developers access to specific test databases while protecting production databases.
- **Service separation**: Restrict microservices to their designated databases.
- **Security compliance**: Enforce database-level access controls as part of your security policy.

#### Database Selector Notes

- Database selectors are a **Dragonfly-specific extension** and are not part of standard Redis ACL.
- The database selector can be combined with other ACL rules (command, key, and pub/sub permissions).
- Database restriction applies to all commands executed by the user.
- Users attempting to access a non-permitted database will receive an ACL permission error.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` on success. If the rules contain errors, the error is returned.

## Examples

### Create a New User with Specific Rules

Create a user with various rules as explained above:

```shell
dragonfly> ACL SETUSER myuser ON >mypass >mysecondpass ~my*key &chan*el +@string +@fast -@slow ~*
OK
```

### Restrict User to Database(s) Using Database Selector

User `alice` can only access database `0`:

```shell
dragonfly> ACL SETUSER alice ON >password ~* +@all $0
OK
```

User `bob` is configured to access database `3` only.
Trying to access any other database with user `bob` will result in an error:

```shell
dragonfly> ACL SETUSER bob ON >secret ~* +@all $3
OK
dragonfly> AUTH bob secret
OK
dragonfly> SELECT 0
(error) NOPERM bob has no ACL permissions
```

User `charlie` can access all available databases:

```shell
dragonfly> ACL SETUSER charlie ON >pass123 ~* +@all $all
OK
```

Verify the users and their database restrictions using `ACL LIST`:

```shell
dragonfly> ACL LIST
1) "user default on nopass ~* &* +@all $all"
2) "user alice on #... ~* &* +@all $0"
3) "user bob on #... ~* &* +@all $3"
4) "user charlie on #... ~* &* +@all $all"
```
