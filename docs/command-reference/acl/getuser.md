---
description: Print ACL's of a user
---

import PageTitle from '@site/src/components/PageTitle';

# ACL GETUSER

<PageTitle title="Redis ACL GETUSER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ACL GETUSER` command in Redis is used to retrieve the details of a specific user in the Access Control List (ACL) system. This command helps administrators manage and review user permissions, commands allowed or denied, and key patterns accessible by the user. It's typically employed in scenarios where user access needs auditing or adjustments.

## Syntax

```plaintext
ACL GETUSER <username>
```

## Parameter Explanations

- `<username>`: The name of the user whose ACL details you want to fetch. It must be a valid username that exists within the Redis ACL configuration.

## Return Values

The command returns an array with details about the specified user. The array includes information such as flags, passwords, allowed commands, and accessible key patterns. For example:

```plaintext
1) "flags"
2) 1) "on"
3) "passwords"
4) 1) "e5d1a9b0767f35a8bbf29d2aba659ace0dbce1c6"
5) "commands"
6) "+@all"
7) "keys"
8) 1) "*"
9) "channels"
10) 1) "*"
```

## Code Examples

```cli
dragonfly> ACL SETUSER john ON >password +@all ~*
OK
dragonfly> ACL GETUSER john
1) "flags"
2) 1) "on"
3) "passwords"
4) 1) "bf85b0cd5d45fd141dd3d2b95c7dc5e7f3bc89a5"
5) "commands"
6) "+@all"
7) "keys"
8) 1) "*"
9) "channels"
10) 1) "*"
```

## Best Practices

- Regularly review user ACLs to ensure that permissions align with current security policies.
- Combine `ACL GETUSER` with other ACL commands like `ACL SETUSER` and `ACL LIST` to effectively manage user permissions.

## Common Mistakes

- Not specifying an existing username will result in an error. Ensure the user exists before attempting to get their details.
- Misinterpreting the returned data structure. Familiarize yourself with the output format for accurate audit and management.

## FAQs

### What happens if I request details for a non-existent user?

Requesting details for a non-existent user will return an error indicating that the user does not exist.

### Can I use wildcards in the username parameter?

No, wildcards cannot be used in the username parameter. You must specify the exact username.

### How can I check all users in the ACL system?

Use the `ACL LIST` command to view a list of all users along with their respective flags and permissions.
