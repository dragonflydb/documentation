---
description: Learn how to use Redis SLOWLOG command to manage the Redis server slowlog.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG

<PageTitle title="Redis SLOWLOG Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SLOWLOG` command in Redis is used to help diagnose performance issues by logging commands that exceed a specified execution time. This tool is useful for identifying slow-running queries, debugging, and optimizing performance.

## Syntax

```cli
SLOWLOG subcommand [argument]
```

## Parameter Explanations

- `subcommand`: The specific operation to be performed on the slow log. Common subcommands include:
  - `GET [count]`: Retrieves the slow log entries, optionally limiting the number of entries returned.
  - `LEN`: Returns the length of the slow log.
  - `RESET`: Clears all entries from the slow log.

## Return Values

- `SLOWLOG GET [count]`: An array of slow log entries, each entry consisting of an entry ID, timestamp, execution time (in microseconds), and the executed command.
- `SLOWLOG LEN`: An integer indicating the number of entries in the slow log.
- `SLOWLOG RESET`: A simple string reply indicating success, usually "OK".

## Code Examples

```cli
dragonfly> SLOWLOG GET 2
1) 1) (integer) 10
   2) (integer) 1625077765
   3) (integer) 1500
   4) 1) "SET"
      2) "key"
      3) "value"
2) 1) (integer) 8
   2) (integer) 1625077705
   3) (integer) 2000
   4) 1) "HSET"
      2) "hash"
      3) "field"
      4) "value"

dragonfly> SLOWLOG LEN
(integer) 5

dragonfly> SLOWLOG RESET
"OK"
```

## Best Practices

- Regularly monitor the slow log to catch performance issues early.
- Adjust the `slowlog-log-slower-than` configuration parameter to an appropriate threshold based on your application's performance requirements.

## Common Mistakes

- Failing to clear the slow log (`SLOWLOG RESET`) can result in an excessively large log if not monitored regularly.
- Misinterpreting the execution time; it is measured in microseconds, not milliseconds.

## FAQs

### How do I configure what constitutes a "slow" query?

You can set the `slowlog-log-slower-than` configuration parameter in your `redis.conf` file or at runtime using the `CONFIG SET` command.

### What is the default length of the slow log?

The default length of the slow log is 128 entries. You can adjust this using the `slowlog-max-len` configuration parameter.
