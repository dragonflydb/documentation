---
description: Print ACL categories and per-group commands
---

import PageTitle from '@site/src/components/PageTitle';

# ACL CAT

<PageTitle title="Redis ACL CAT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ACL CAT` command in Redis is used to list available categories of commands that can be assigned to users through Access Control Lists (ACLs). This helps administrators manage permissions by grouping related commands together.

Typical scenarios where `ACL CAT` is used include:

- Determining which command categories exist for better role management.
- Reviewing available categories when setting up or modifying user access controls.

## Syntax

```plaintext
ACL CAT [<category>]
```

## Parameter Explanations

- `<category>`: Optional. If specified, the command will return commands belonging to the given category. If omitted, it lists all available categories.

## Return Values

- Without `<category>`: Returns an array of strings, each representing a command category.
- With `<category>`: Returns an array of strings listing all commands within the specified category.

Example outputs:

```plaintext
1) "keyspace"
2) "read"
3) "write"
4) "set"
... (other categories listed)
```

or

```plaintext
1) "GET"
2) "SET"
3) "DEL"
... (commands in the specified category)
```

## Code Examples

```cli
dragonfly> ACL CAT
1) "keyspace"
2) "read"
3) "write"
4) "set"
5) "sortedset"

dragonfly> ACL CAT read
1) "GET"
2) "MGET"
3) "EXISTS"
4) "TYPE"
5) "SCAN"
```

## Best Practices

When managing ACLs, always start by understanding the available categories through `ACL CAT`. This ensures you make informed decisions about which categories of commands to assign to different user roles.

## Common Mistakes

### Misinterpreting Categories

A common mistake is to assume what commands fall under each category without checking. Always use `ACL CAT <category>` to verify the exact commands within a category.

## FAQs

### What happens if I specify a non-existent category?

If you specify a category that does not exist, Redis returns an empty array.

### Is `ACL CAT` available in all versions of Redis?

`ACL CAT` was introduced in Redis 6.0. Ensure you are running Redis 6.0 or later to use this command.
