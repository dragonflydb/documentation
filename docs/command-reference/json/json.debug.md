---
description: Discover Redis JSON.DEBUG command for detailed debugging information about JSON values.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.DEBUG

<PageTitle title="Redis JSON.DEBUG Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.DEBUG` is a command used in Redis to inspect and debug JSON data stored using the RedisJSON module. This command helps users understand the structure and metadata of their JSON documents, which is essential for troubleshooting and optimizing data storage.

## Syntax

```cli
JSON.DEBUG <subcommand> <key> [path]
```

## Parameter Explanations

- **subcommand**: The specific debugging operation to perform. Common subcommands include `MEMORY` to check memory usage and `HELP` to get more information on the command.
- **key**: The key under which the JSON document is stored.
- **path**: (Optional) A JSONPath expression to specify a particular part of the JSON document.

## Return Values

The return value varies based on the subcommand:

- `MEMORY`: Returns the memory usage of the JSON value at the specified path.
- `HELP`: Lists all available subcommands and their descriptions.

### Examples of Possible Outputs

- For `MEMORY`:
  ```cli
  "1234"
  ```
- For `HELP`:
  ```cli
  "MEMORY - Report memory usage\nHELP - Show information about the JSON.DEBUG command"
  ```

## Code Examples

```cli
dragonfly> JSON.SET myjson . '{"name": "Alice", "age": 30}'
OK
dragonfly> JSON.DEBUG MEMORY myjson .
"56"
dragonfly> JSON.DEBUG HELP
1) "MEMORY - Report memory usage"
2) "HELP - Show information about the JSON.DEBUG command"
```

## Best Practices

- Use `JSON.DEBUG MEMORY` to monitor the memory consumption of large JSON documents. This can help identify performance bottlenecks and optimize your data storage strategy.

## Common Mistakes

- Omitting the `path` parameter when it is necessary for detailed inspection can lead to incomplete information.
- Using `JSON.DEBUG` without understanding its impact on performance; excessive debugging commands might slow down a busy Redis server.

## FAQs

### What does `JSON.DEBUG MEMORY` report?

It reports the memory usage in bytes of the JSON value at the specified path.

### Can I use `JSON.DEBUG` on non-JSON keys?

No, `JSON.DEBUG` subcommands are specifically designed for JSON data managed by the RedisJSON module.
