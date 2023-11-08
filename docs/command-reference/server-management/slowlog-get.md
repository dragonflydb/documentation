---
description:  Discover how to use Redis SLOWLOG GET command to retrieve the list of slow commands.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG GET

<PageTitle title="Redis SLOWLOG GET Command (Documentation) | Dragonfly" />

## Syntax

    SLOWLOG GET [count]

The `SLOWLOG GET` command returns entries from the slow log in chronological order.

The Dragonfly Slow Log is a system to log queries that exceeded a specified execution time.
The execution time may include I/O operations like talking sending the reply.

A new entry is added to the slow log whenever a command exceeds the execution time threshold
defined by the `slowlog_log_slower_than` configuration directive.
The maximum number of entries in the slow log is governed by the `slowlog_max_len` configuration directive.

By default the command returns latest twenty entries in the log. The optional `count` argument limits the number of returned entries, so the command returns at most up to `count` entries, the special number -1 means return all entries.

Each entry from the slow log is comprised of the following six values:

1. A unique progressive identifier for every slow log entry.
2. The unix timestamp at which the logged command was processed.
3. The amount of time needed for its execution, in microseconds.
4. The array composing the arguments of the command.
5. Client IP address and port.
6. Client name if set via the `CLIENT SETNAME` command.

The entry's unique ID can be used in order to avoid processing slow log entries multiple times (for instance you may have a script sending you an email alert for every new slow log entry).
The ID is never reset in the course of the Dragonfly server execution, only a server
restart will reset it.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of slow log entries.
