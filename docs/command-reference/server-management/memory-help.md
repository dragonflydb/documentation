---
description: Learn how to use Redis MEMORY HELP command to know all the MEMORY subcommands.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY HELP

<PageTitle title="Redis MEMORY HELP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MEMORY HELP` command in Redis provides a list of subcommands related to memory usage, offering guidance on how to understand and optimize memory consumption. This command is particularly useful for developers and system administrators who need to monitor and manage the memory footprint of their Redis instances.

## Syntax

```plaintext
MEMORY HELP
```

## Parameter Explanations

The `MEMORY HELP` command does not take any parameters. It simply returns a list of available subcommands under the `MEMORY` command family, along with brief descriptions of what each subcommand does.

## Return Values

The `MEMORY HELP` command returns an array of strings, where each string provides information about a subcommand related to memory usage. For example:

```plaintext
1) "MEMORY DOCTOR"
2) " - Outputs memory problems report"
3) "MEMORY MALLOC-STATS"
4) " - Show allocator internal stats"
5) "MEMORY PURGE"
6) " - Attempt to purge dirty pages for reuse"
7) "MEMORY STATS"
8) " - Show memory usage details"
9) "MEMORY USAGE <key>"
10) " - Estimate memory usage of key"
```

## Code Examples

```cli
dragonfly> MEMORY HELP
1) "MEMORY DOCTOR"
2) " - Outputs memory problems report"
3) "MEMORY MALLOC-STATS"
4) " - Show allocator internal stats"
5) "MEMORY PURGE"
6) " - Attempt to purge dirty pages for reuse"
7) "MEMORY STATS"
8) " - Show memory usage details"
9) "MEMORY USAGE <key>"
10) " - Estimate memory usage of key"
```

## Best Practices

- Regularly use `MEMORY HELP` to familiarize yourself with the available tools for monitoring and managing memory in Redis.
- Combine `MEMORY HELP` with other `MEMORY` subcommands like `MEMORY STATS` and `MEMORY DOCTOR` to get a comprehensive view of your instance’s memory health.

## Common Mistakes

- Ignoring the output of `MEMORY HELP` and underutilizing the full suite of memory management tools provided by Redis.
- Misinterpreting the purpose of `MEMORY HELP`; it is an informational command and does not perform any memory diagnostics or optimizations by itself.

## FAQs

### What is the purpose of `MEMORY HELP`?

`MEMORY HELP` provides a list of memory-related subcommands in Redis and brief descriptions of their functionalities, helping users to understand and utilize these commands effectively.

### Can `MEMORY HELP` be used to diagnose memory issues directly?

No, `MEMORY HELP` only lists subcommands. To diagnose memory issues, use `MEMORY DOCTOR` or other relevant subcommands listed by `MEMORY HELP`.
