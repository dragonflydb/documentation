---
description: Save the current ACL rules in the configured ACL file
---

# ACL SAVE

## Syntax

    ACL SAVE 

**Time complexity:** O(N). Where N is the number of configured users.

When Redis is configured to use an ACL file (with the `aclfile` configuration
option), this command will save the currently defined ACLs from the server memory to the ACL file.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK` on success.

The command may fail with an error for several reasons: if the file cannot be written or if the server is not configured to use an external ACL file.

## Examples

```
> ACL SAVE
+OK

> ACL SAVE
-ERR There was an error trying to save the ACLs. Please check the server logs for more information
```
