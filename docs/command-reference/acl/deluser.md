---
description: "Learn how to use Redis ACL DELUSER to remove specified users from the Access Control List and enhance database security."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL DELUSER

<PageTitle title="Redis ACL DELUSER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`ACL DELUSER` is a Redis command used to delete user accounts from the ACL (Access Control List) system. This command is critical for managing security and permissions within your Redis instance. Typical use cases include removing outdated or compromised user accounts, and maintaining a clean and secure user environment.

## Syntax

```
ACL DELUSER username [username ...]
```

## Parameter Explanations

- `username`: The name of the user(s) you wish to delete. You can specify multiple usernames separated by spaces.

## Return Values

The command returns the number of users that were successfully removed.

Example outputs:

- `(integer) 1` if one user was deleted.
- `(integer) 0` if no users were found with the specified names.

## Code Examples

```cli
dragonfly> ACL LIST
1) "user default on nopass ~* +@all"
2) "user guest off nopass ~* -@all"
3) "user admin on >password ~* +@all"
dragonfly> ACL DELUSER guest
(integer) 1
dragonfly> ACL LIST
1) "user default on nopass ~* +@all"
2) "user admin on >password ~* +@all"
dragonfly> ACL DELUSER nonexistinguser
(integer) 0
```

## Best Practices

- Always ensure you are deleting the correct user by listing users with `ACL LIST` before deletion.
- Regularly review your ACL to remove any redundant or unnecessary users.

## Common Mistakes

- Attempting to delete a user that does not exist will return `(integer) 0` and may lead to confusion. Double-check usernames before executing the command.

## FAQs

### What happens if I try to delete multiple users at once and some do not exist?

The command will still execute and delete the existing users, returning the count of users that were actually deleted.

### Can I delete the default user?

No, the default user cannot be deleted. It is a built-in account necessary for Redis operation.
