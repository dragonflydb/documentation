---
description: "Learn how to use Redis ACL WHOAMI to return the name of the authenticated user."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL WHOAMI

<PageTitle title="Redis ACL WHOAMI Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`ACL WHOAMI` is a command used in Redis to determine the current username of the authenticated connection. It is particularly useful for debugging purposes, auditing user permissions, and ensuring that the correct user context is applied within a session.

## Syntax

```cli
ACL WHOAMI
```

## Parameter Explanations

This command does not accept any parameters.

## Return Values

The command returns a simple string with the current authenticated username.

Example outputs:

- If the user `default` is authenticated: `"default"`
- If a custom user `admin` is authenticated: `"admin"`

## Code Examples

```cli
dragonfly> ACL WHOAMI
"default"
dragonfly> AUTH admin mypassword
OK
dragonfly> ACL WHOAMI
"admin"
```

## Best Practices

It’s a good practice to use `ACL WHOAMI` in scripts or debugging sessions to verify the authenticated user, especially when working with multiple users having different permission sets.

## Common Mistakes

### Misinterpreting the Output

- Ensure you understand that the output indicates the user context under which the current connection operates. This might differ from what you expect if the authentication commands were mismanaged.
