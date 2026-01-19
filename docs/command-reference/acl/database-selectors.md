---
description: "Restrict user access to specific logical databases using ACL database selectors"
---

import PageTitle from '@site/src/components/PageTitle';

# ACL Database Selectors

<PageTitle title="ACL Database Selectors (Documentation) | Dragonfly" />

## Overview

Dragonfly ACL supports **database selectors**, a Dragonfly-specific feature that allows you to restrict user access to specific logical databases. This provides fine-grained control over which databases authenticated users can access.

## Syntax

Database selectors are specified as part of the `ACL SETUSER` command using the `$` prefix:

    ACL SETUSER username $<database>
    ACL SETUSER username $all

## Database Selector Rules

- `$<database>`: Restricts the user to access only the specified database number. For example, `$0` restricts to database 0, `$1` to database 1, etc.
- `$all`: Allows the user to access all databases (default behavior).

## Behavior

- When a user is restricted to a specific database, they can only execute commands on that database
- Attempting to `SELECT` a different database or access keys in a non-permitted database will result in an error
- The database number must be less than the configured `--dbnum` value
- By default, if no database selector is specified, users have access to all databases (`$all`)

## Examples

### Restrict User to Database 0

```shell
dragonfly> ACL SETUSER alice ON >password ~* +@all $0
OK
```

User `alice` can only access database 0.

### Restrict User to Database 3

```shell
dragonfly> ACL SETUSER bob ON >secret ~* +@all $3
OK
```

User `bob` can only access database 3.

### Allow Access to All Databases

```shell
dragonfly> ACL SETUSER charlie ON >pass123 ~* +@all $all
OK
```

User `charlie` can access all available databases.

### View User Database Restrictions

```shell
dragonfly> ACL LIST
1) "user default on nopass ~* &* +@all $all"
2) "user alice on #... ~* &* +@all $0"
3) "user bob on #... ~* &* +@all $3"
4) "user charlie on #... ~* &* +@all $all"
```

## Use Cases

- **Multi-tenancy**: Isolate different tenants or applications by assigning each to a dedicated database
- **Development environments**: Give developers access to specific test databases while protecting production databases
- **Service separation**: Restrict microservices to their designated databases
- **Security compliance**: Enforce database-level access controls as part of your security policy

## Notes

- Database selectors are a **Dragonfly-specific extension** and are not part of standard Redis ACL
- The database selector can be combined with other ACL rules (command, key, and pub/sub permissions)
- Database restriction applies to all commands executed by the user
- Users attempting to access a non-permitted database will receive an ACL permission error

## See Also

- [ACL SETUSER](setuser.md) - Modify or create user rules
- [ACL LIST](list.md) - List all users and their ACL rules
- [ACL GETUSER](getuser.md) - Get specific user ACL rules
