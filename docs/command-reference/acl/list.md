---
description: "Learn how to use Redis ACL LIST to retrieve the list of rules for all the existing users."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL LIST

<PageTitle title="Redis ACL LIST Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ACL LIST` command in Redis is used to retrieve the currently active Access Control List (ACL) rules. These rules define the permissions for different users and their ability to execute commands within the Redis instance. Typical use cases include auditing current ACL configurations, troubleshooting user permission issues, and verifying the correct implementation of security policies.

## Syntax

```
ACL LIST
```

## Parameter Explanations

The `ACL LIST` command does not take any parameters.

## Return Values

The `ACL LIST` command returns an array of strings, where each string represents a single ACL rule. Each rule includes details such as user names, allowed commands, denied commands, and key patterns they can access.

### Example Output

```plaintext
1) "user default on nopass ~* +@all"
2) "user alice on >password ~* +@read -@write"
3) "user bob off"
```

## Code Examples

```cli
dragonfly> ACL LIST
1) "user default on nopass ~* +@all"
2) "user alice on >password ~* +@read -@write"
3) "user bob off"
```

## Best Practices

- Regularly audit your ACL configurations using `ACL LIST` to ensure that only necessary permissions are granted.
- Combine this command with other ACL commands like `ACL SETUSER` and `ACL GETUSER` to manage and verify user permissions effectively.

## Common Mistakes

- Forgetting that the `ACL LIST` output may change if the ACL configuration is modified by another administrator concurrently.
- Misinterpreting the output format, especially when dealing with complex permissions or multiple users.

## FAQs

### What do the symbols in the ACL LIST output mean?

- The plus (`+`) indicates allowed commands or command categories.
- The minus (`-`) indicates denied commands or command categories.
- The tilde (`~`) specifies key patterns the user can access.
- The greater-than sign (`>`) before a password signifies the hashed password.

### How can I use the information from ACL LIST?

Use the data to verify user permissions, identify potential security risks, and ensure compliance with security policies by comparing actual configurations against expected ones.
