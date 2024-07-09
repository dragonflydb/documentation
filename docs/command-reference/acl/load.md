---
description: Load all ACL configuration from a file
---

import PageTitle from '@site/src/components/PageTitle';

# ACL LOAD

<PageTitle title="Redis ACL LOAD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`ACL LOAD` is a Redis command used to reload the ACL (Access Control List) configuration from the `aclfile`. This is crucial when changes are made directly to the ACL file, allowing those modifications to be applied without restarting the Redis server. Typical scenarios include updating user permissions or roles in environments where Redis security is tightly controlled.

## Syntax

```plaintext
ACL LOAD
```

## Parameter Explanations

`ACL LOAD` does not take any parameters. It simply reads the `aclfile` defined in the Redis configuration and applies its rules immediately.

## Return Values

The command returns a simple status reply:

- `OK` if the ACL rules were successfully reloaded.
- An error message if there was an issue loading the ACL file.

## Code Examples

```cli
dragonfly> ACL LOAD
"OK"
```

## Best Practices

- Ensure the `aclfile` is correctly formatted and validated before using `ACL LOAD` to avoid errors.
- Regularly back up your ACL configurations to prevent accidental loss or corruption.

## Common Mistakes

- Forgetting to save the `aclfile` after editing it. If the file is not saved, `ACL LOAD` will reload the old configuration.
- Misconfiguring the `aclfile` path in the Redis configuration, which can lead to errors when attempting to load the ACL rules.

## FAQs

### What happens if there is an error in the `aclfile`?

Redis will return an error message indicating that the ACL rules could not be loaded. You need to correct the errors in the `aclfile` and try `ACL LOAD` again.

### Does `ACL LOAD` require a server restart?

No, `ACL LOAD` allows you to apply changes to the access control list without restarting the Redis server.
