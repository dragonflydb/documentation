---
description: "Learn how to use Redis ACL SETUSER to modify or create new user rules in the Access Control List."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL SETUSER

<PageTitle title="Redis ACL SETUSER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ACL SETUSER` command in Redis is used to create or modify a user in the ACL (Access Control List) system. This command allows administrators to define user permissions, including what commands users can run and which keys they can access. It is typically used in scenarios where multiple users need different levels of access to a Redis database.

## Syntax

```plaintext
ACL SETUSER <username> [rule [rule ...]]
```

## Parameter Explanations

- `<username>`: The name of the user you want to create or modify.
- `[rule [rule ...]]`: One or more rules defining the user's permissions. Rules include:
  - `on` / `off`: Enable or disable the user.
  - `+<command>`: Allow specific command(s).
  - `-<command>`: Disallow specific command(s).
  - `~<pattern>`: Allow access to keys matching a given pattern.
  - `resetkeys`: Remove all key patterns.
  - `resetcommands`: Remove all command rules.
  - `allkeys`: Grant access to all keys.
  - `allcommands`: Allow all commands.

## Return Values

The `ACL SETUSER` command returns a simple string reply indicating the result of setting the user's permissions. For example:

```plaintext
OK
```

## Code Examples

```cli
dragonfly> ACL SETUSER alice on +get +set ~foo:* -debug
"OK"
dragonfly> ACL SETUSER bob off
"OK"
dragonfly> ACL SETUSER charlie resetkeys resetcommands
"OK"
dragonfly> ACL LIST
1) "user default on nopass ~* +@all"
2) "user alice on #5edabdbf39e5ccb7c3d8aa7ba97dc9ef40de7f08bfe4c85f63d70ec6b5a9ad14 +get +set ~foo:* -debug"
3) "user bob off"
4) "user charlie on resetkeys resetcommands"
```

## Best Practices

- Regularly review and update user permissions to ensure security.
- Use specific key patterns (`~<pattern>`) instead of granting access to all keys.
- Disable users (`off`) when they no longer need access instead of deleting them immediately.

## Common Mistakes

- Forgetting to enable the user with `on` after creating it.
- Overusing `allcommands` or `allkeys`, which may lead to unintentional security risks.

## FAQs

### How do I disable a user without deleting them?

Use the `off` rule:

```cli
dragonfly> ACL SETUSER username off
"OK"
```

### Can I reset all rules for a user?

Yes, use `resetkeys` and `resetcommands`:

```cli
dragonfly> ACL SETUSER username resetkeys resetcommands
"OK"
```
