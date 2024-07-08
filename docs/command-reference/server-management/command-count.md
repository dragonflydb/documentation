---
description: Learn how to use Redis COMMAND COUNT to count the total number of commands.
---

import PageTitle from '@site/src/components/PageTitle';

# COMMAND COUNT

<PageTitle title="Redis COMMAND COUNT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `COMMAND COUNT` command in Redis provides the total number of available commands in the Redis server. This is particularly useful for administrators or developers who need to audit or interact with the complete set of Redis commands dynamically.

## Syntax

```cli
COMMAND COUNT
```

## Parameter Explanations

This command does not take any parameters.

## Return Values

The `COMMAND COUNT` command returns an integer representing the total number of commands available in the current Redis server instance.

**Example Output:**

```cli
(integer) 179
```

## Code Examples

```cli
dragonfly> COMMAND COUNT
(integer) 179
```

## Best Practices

- Use `COMMAND COUNT` to verify compatibility when working with different Redis versions or custom modules that may add additional commands.
- Combine with `COMMAND INFO` and `COMMAND LIST` to get comprehensive details about each command.

## Common Mistakes

- Running `COMMAND COUNT` on older Redis versions that might not support this command can result in errors. Always ensure your Redis server version supports the command before using it.

## FAQs

### What Redis version introduced the `COMMAND COUNT` command?

The `COMMAND COUNT` command was introduced in Redis version 2.8.13.

### Can I use `COMMAND COUNT` to get details about specific commands?

No, `COMMAND COUNT` only returns the total number of available commands. To get details about specific commands, use `COMMAND INFO`.
