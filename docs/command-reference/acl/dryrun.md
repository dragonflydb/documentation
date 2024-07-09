---
description: Simulate execution of a command from a user
---

import PageTitle from '@site/src/components/PageTitle';

# ACL DRYRUN

<PageTitle title="Redis ACL DRYRUN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ACL DRYRUN` command in Redis is used to simulate the execution of a given command by a user, checking if the user has the necessary permissions according to the specified Access Control List (ACL) rules. This command is helpful for debugging and verifying ACL configurations without actually executing the commands.

## Syntax

```
ACL DRYRUN <username> <command>
```

## Parameter Explanations

- **username**: The name of the user whose ACL permissions are to be checked.
- **command**: The command that you want to simulate execution for. This includes the command and its arguments.

## Return Values

This command returns a simple string. It will respond with:

- `"OK"` if the user has permission to execute the command.
- An error message if the user lacks the necessary permissions, indicating which rule blocked the command.

## Code Examples

```cli
dragonfly> ACL SETUSER alice on >password ~* +@all
OK
dragonfly> ACL DRYRUN alice "GET mykey"
"OK"
dragonfly> ACL DELUSER alice
(integer) 1
dragonfly> ACL DRYRUN alice "SET mykey value"
(error) ERR User does not exist or this user has no permissions
```

## Common Mistakes

- **Incorrect Username**: Using a username that doesn't exist will result in an error.
- **Improper Command Format**: Ensure the command string is correctly formatted and encapsulated in quotes if it contains spaces.

### Why did I get an ERR User does not exist or this user has no permissions?

This error occurs if the specified user doesn't exist or if the user has no assigned permissions. Double-check the user's creation status and their associated permissions.
