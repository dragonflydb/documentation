---
description: Learn how to use Redis AUTH command for server authentication.
---

import PageTitle from '@site/src/components/PageTitle';

# AUTH

<PageTitle title="Redis AUTH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `AUTH` command in Redis is used to authenticate a client connection using a password. This is essential for securing Redis servers by ensuring that only clients with the correct credentials can interact with the database. Typical scenarios include setting up password-protected access to production Redis instances or implementing multi-user environments.

## Syntax

```plaintext
AUTH [username] password
```

## Parameter Explanations

- **username**: Optional. The username of the Redis user when using ACLs (Access Control Lists). If omitted, Redis uses the default user.
- **password**: Required. The password associated with the user or the default password if no username is provided.

## Return Values

- **OK**: Authentication was successful.
- **(error)**: Authentication failed due to incorrect password or other issues.

Examples:

- `OK`
- `(error) ERR invalid password`

## Code Examples

```cli
dragonfly> AUTH mypassword
OK
dragonfly> AUTH wrongpassword
(error) ERR invalid password
dragonfly> AUTH defaultuser mypassword
OK
dragonfly> AUTH defaultuser wrongpassword
(error) ERR invalid password
```

## Best Practices

- Always use strong, complex passwords to secure your Redis instances.
- Implement ACLs for more granular control over user permissions.

## Common Mistakes

- Not changing the default password, which poses a significant security risk.
- Forgetting to use the correct format when ACLs are enabled, i.e., providing both username and password.

## FAQs

### What happens if I omit the username in the AUTH command?

If you omit the username, Redis will authenticate using the default user.

### Can I change the password without restarting Redis?

Yes, you can update the password dynamically using the `CONFIG SET` command or through ACLs.

### Is it possible to disable authentication?

By not setting a `requirepass` or configuring ACLs, Redis will not require authentication. However, this is not recommended for production environments.
