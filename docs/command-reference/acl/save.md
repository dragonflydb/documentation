---
description: Persist currently defined ACL's to file
---

import PageTitle from '@site/src/components/PageTitle';

# ACL SAVE

<PageTitle title="Redis ACL SAVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`ACL SAVE` command in Redis is used to persist the current Access Control List (ACL) rules to the `aclfile`. This command is crucial for ensuring that any changes made to the ACL rules are saved and not lost upon server restarts. Typical scenarios include updating user permissions and needing to make sure these updates are saved.

## Syntax

```
ACL SAVE
```

## Parameter Explanations

The `ACL SAVE` command does not take any parameters.

## Return Values

The command returns a simple string reply indicating whether the operation was successful.

- `(simple string) OK`: The ACL rules were successfully saved to the file.
- An error message may be returned if the operation fails, detailing the issue.

## Code Examples

```cli
dragonfly> ACL SAVE
"OK"
```

## Best Practices

- Always use `ACL SAVE` after making changes to your ACLs to ensure they are persisted.
- Regularly back up your `aclfile` to avoid loss of critical security configurations.

## Common Mistakes

- Forgetting to execute `ACL SAVE` after modifying ACL rules can result in loss of those changes upon server restart.

## FAQs

### What happens if I do not use `ACL SAVE` after modifying ACL rules?

If you do not save the ACL rules after modifications, the changes will not persist after the Redis server is restarted, leading to potential security risks.

### Can `ACL SAVE` fail?

Yes, `ACL SAVE` can fail if there are issues with writing to the `aclfile`, such as permission errors or disk space issues. Ensure that Redis has the necessary permissions and sufficient disk space.
