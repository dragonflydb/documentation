---
description: Get an array of Redis command names
---

# COMMAND LIST

## Syntax

    COMMAND LIST [FILTERBY <MODULE module-name | ACLCAT category | PATTERN pattern>]

**Time complexity:** O(N) where N is the total number of Redis commands

Return an array of the server's command names.

You can use the optional _FILTERBY_ modifier to apply one of the following filters:

 - **MODULE module-name**: get the commands that belong to the module specified by _module-name_.
 - **ACLCAT category**: get the commands in the [ACL category](https://redis.io/docs/management/security/acl/#command-categories) specified by _category_.
 - **PATTERN pattern**: get the commands that match the given glob-like _pattern_.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): a list of command names.
