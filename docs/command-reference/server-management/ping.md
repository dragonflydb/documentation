---
description: Learn how to use Redis PING command to check the server's status.
---

import PageTitle from '@site/src/components/PageTitle';

# PING

<PageTitle title="Redis PING Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PING` command in Redis is used to check the connection to the server. It’s a simple way to verify that the server is running and responding. It's commonly used in health checks, monitoring scripts, or client libraries to ensure the connection to the Redis server is alive.

## Syntax

```plaintext
PING [message]
```

## Parameter Explanations

- `message`: An optional parameter. If provided, Redis will return this message instead of the default "PONG".

## Return Values

- Without the `message` parameter: Returns the string "PONG".
- With the `message` parameter: Returns the message provided as input.

## Code Examples

```cli
dragonfly> PING
"PONG"
dragonfly> PING "Hello, Redis!"
"Hello, Redis!"
```

## Best Practices

- Use `PING` periodically in your application to ensure the Redis connection is healthy.
- Combine `PING` with other monitoring commands to get a comprehensive view of server health.

## Common Mistakes

- Overusing `PING` can add unnecessary load to your Redis server. Use it judiciously within your monitoring or health check routines.

## FAQs

### Is `PING` useful for checking latency?

No, `PING` is primarily for connectivity checks. For latency measurements, consider using the `LATENCY DOCTOR` command.

### Can `PING` be used in Redis Cluster?

Yes, `PING` works the same way in Redis Cluster as it does in a standalone Redis instance.
