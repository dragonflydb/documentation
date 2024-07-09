---
description: Learn how to use Redis `JSON.DEBUG HELP` to understand how to troubleshoot JSON objects with this command.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.DEBUG HELP

<PageTitle title="Redis `JSON.DEBUG HELP` Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `JSON.DEBUG HELP` command in Redis is part of the RedisJSON module. It provides debugging help information related to JSON structures stored in Redis. This command is useful for developers who need to understand how to debug issues with their JSON data within Redis.

## Syntax

```plaintext
JSON.DEBUG HELP
```

## Parameter Explanations

This command does not take any parameters. It simply returns a list of subcommands available under the `JSON.DEBUG` namespace along with brief descriptions.

## Return Values

The command returns an array of strings, where each string is a line of helpful information regarding JSON debugging commands.

### Example Output

```plaintext
1) "DEBUG MEMORY <key> [path]"
2) "    Report memory usage"
3) ""
4) "DEBUG HELP"
5) "    this message"
```

## Code Examples

```cli
dragonfly> JSON.DEBUG HELP
1) "DEBUG MEMORY <key> [path]"
2) "    Report memory usage"
3) ""
4) "DEBUG HELP"
5) "    this message"
```

## Best Practices

- Regularly use `JSON.DEBUG HELP` to familiarize yourself with available debugging tools.
- Combine this command with other `JSON.DEBUG` commands to effectively troubleshoot JSON issues in Redis.

## Common Mistakes

- Misunderstanding the scope: This command provides help information only for JSON debugging and does not perform any modification or retrieval of JSON data.
