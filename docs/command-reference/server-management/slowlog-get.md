---
description: Discover how to use Redis SLOWLOG GET command to retrieve the list of slow commands.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG GET

<PageTitle title="Redis SLOWLOG GET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`SLOWLOG GET` is a command in Redis used to fetch entries from the slow query log. This command is especially useful for monitoring and debugging performance issues by identifying commands that are taking longer than expected to execute.

## Syntax

```cli
SLOWLOG GET [count]
```

## Parameter Explanations

- `count`: Optional. Specifies the number of slow log entries to retrieve. If not provided, all entries are fetched.

## Return Values

The command returns an array of slow log entries. Each entry is itself an array containing four elements:

1. An incremental unique identifier for every slow log entry.
2. The unix timestamp at which the logged command was processed.
3. The amount of time needed for its execution, in microseconds.
4. The array representing the arguments of the command executed.

Example output:

```cli
1) 1) (integer) 12
   2) (integer) 1625069120
   3) (integer) 15000
   4) 1) "SET"
      2) "key"
      3) "value"
```

## Code Examples

```cli
dragonfly> SLOWLOG GET
1) 1) (integer) 15
   2) (integer) 1625764978
   3) (integer) 12345
   4) 1) "GET"
      2) "mykey"
2) 1) (integer) 14
   2) (integer) 1625764965
   3) (integer) 6789
   4) 1) "HMSET"
      2) "myhash"
      3) "field1"
      4) "value1"

dragonfly> SLOWLOG GET 1
1) 1) (integer) 15
   2) (integer) 1625764978
   3) (integer) 12345
   4) 1) "GET"
      2) "mykey"
```

## Best Practices

- Regularly check the slow log to keep track of any long-running commands.
- Adjust Redis configurations or optimize queries based on insights from the slow log.

## Common Mistakes

- Not specifying a `count` may return a very large number of entries, which can be overwhelming. Use the `count` parameter to limit the results for easier analysis.

## FAQs

### What happens if I don't provide a count?

If no count is specified, `SLOWLOG GET` returns all available slow log entries.

### How can I clear the slow log?

Use the `SLOWLOG RESET` command to clear the slow log.
