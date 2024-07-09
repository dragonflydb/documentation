---
description: Print the usernames of all users
---

import PageTitle from '@site/src/components/PageTitle';

# ACL USERS

<PageTitle title="Redis ACL USERS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ACL USERS` command in Redis is used to retrieve a list of all user names defined in the Access Control List (ACL) system. This is particularly useful for administrators looking to manage or audit existing users, ensuring proper permissions are set or identifying unused accounts.

## Syntax

```plaintext
ACL USERS
```

## Parameter Explanations

This command does not take any parameters. It simply lists all the existing ACL users.

## Return Values

The `ACL USERS` command returns an array of strings, each representing a user name. For example:

```plaintext
1) "default"
2) "admin"
3) "guest"
```

## Code Examples

```cli
dragonfly> ACL USERS
1) "default"
2) "alice"
3) "bob"
```

## Best Practices

- Regularly review the output of `ACL USERS` to ensure no unauthorized users have been added.
- Combine with other ACL commands like `ACL GETUSER` to verify permissions and roles assigned to each user.

## Common Mistakes

- Forgetting to review this list periodically, which can lead to security issues if old or unnecessary users are not removed.
- Misunderstanding the scope of returned users; it only lists user names without details on their permissions or roles.

## FAQs

### What does the default user mean in Redis ACL?

The "default" user is a built-in user that always exists and cannot be deleted. Administrators should configure its permissions carefully as part of the security setup.
