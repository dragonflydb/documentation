---
description: Discover how to use Redis SLOWLOG HELP command to retrieve the current number of entries in the slow log.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG HELP

<PageTitle title="Redis SLOWLOG HELP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SLOWLOG HELP` command in Redis provides information about the subcommands available for managing the Slow Log feature. The Slow Log is used to log queries that exceed a specified execution time threshold, helping identify performance bottlenecks.

## Syntax

```plaintext
SLOWLOG HELP
```

## Parameter Explanations

The `SLOWLOG HELP` command does not take any parameters.

## Return Values

The command returns an array of strings where each string describes a specific subcommand related to the Slow Log. For example:

```plaintext
1) "SLOWLOG <subcommand> [argument [arguments ...]]"
2) "  GET     - return top <count> entries from the slowlog (default: 10)"
3) "  LEN     - return length of slowlog"
4) "  RESET   - reset the slowlog"
5) "  HELP    - show this help"
```

## Code Examples

```cli
dragonfly> SLOWLOG HELP
1) "SLOWLOG <subcommand> [argument [arguments ...]]"
2) "  GET     - return top <count> entries from the slowlog (default: 10)"
3) "  LEN     - return length of slowlog"
4) "  RESET   - reset the slowlog"
5) "  HELP    - show this help"
```

## Best Practices

Using `SLOWLOG HELP` can be particularly useful when you're unfamiliar with the Slow Log's subcommands or need a quick reference without leaving the Redis CLI.

## Common Mistakes

- **Assuming Parameters**: The `SLOWLOG HELP` command does not accept any parameters. Providing parameters will result in an error.
- **Ignoring Output Format**: Not recognizing that the output is an array of strings which need to be parsed to understand the available subcommands.

## FAQs

### What is the primary purpose of the `SLOWLOG` feature?

The `SLOWLOG` feature logs commands that exceed a specified execution time, assisting in identifying and troubleshooting performance issues.

### How often should I check the Slow Log?

Regularly monitoring the Slow Log, especially after deploying new code or configurations, helps quickly identify and resolve performance problems.
