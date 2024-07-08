---
description: Learn how to use Redis MONITOR command to inspect the operations.
---

import PageTitle from '@site/src/components/PageTitle';

# MONITOR

<PageTitle title="Redis MONITOR Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MONITOR` command in Redis is used to stream back every command processed by the Redis server. This command is primarily used for debugging purposes, allowing developers to see real-time interactions between clients and the Redis instance. Typical use cases include tracking down bugs, understanding traffic patterns, and analyzing command usage for optimization.

## Syntax

```
MONITOR
```

## Parameter Explanations

The `MONITOR` command does not take any parameters. Once issued, it starts streaming all commands received by the Redis server to the client that executed the `MONITOR` command.

## Return Values

The `MONITOR` command returns a continuous stream of commands executed by the Redis server. Each command is output as soon as it is received and processed. The return value consists of the exact representation of the command as it was sent to the server.

Examples of possible outputs:

```
1488966955.123456 [0 127.0.0.1:6379] "SET" "key" "value"
1488966955.123789 [0 127.0.0.1:6379] "GET" "key"
```

## Code Examples

```cli
dragonfly> MONITOR
OK
1488966955.123456 [0 127.0.0.1:6379] "SET" "mykey" "hello"
1488966955.123789 [0 127.0.0.1:6379] "GET" "mykey"
1488966955.124000 [0 127.0.0.1:6379] "DEL" "mykey"
```

In another terminal:

```cli
dragonfly> SET mykey "hello"
OK
dragonfly> GET mykey
"hello"
dragonfly> DEL mykey
(integer) 1
```

## Best Practices

- Use the `MONITOR` command sparingly in production environments as it can significantly affect performance due to the high I/O it generates.
- It is advisable to use `MONITOR` only during debugging sessions and turn it off immediately after debugging is completed.

## Common Mistakes

- Executing `MONITOR` in a production environment without understanding the potential performance impact.
- Forgetting to stop the `MONITOR` command, leading to unnecessary resource consumption.

## FAQs

### How do I stop the `MONITOR` command?

Simply close the connection (e.g., exit the CLI session) that is currently running the `MONITOR` command. There is no specific command to stop `MONITOR`; terminating the session will suffice.

### Can multiple clients run `MONITOR` simultaneously?

Yes, multiple clients can run the `MONITOR` command simultaneously. Each client will receive its own stream of commands being processed by the Redis server.
