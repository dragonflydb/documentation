---
description: Learn how to use Redis CLIENT LIST command to fetch details about all client connections.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT LIST

<PageTitle title="Redis CLIENT LIST Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`CLIENT LIST` is a Redis command used to obtain information about all connected clients. This includes details like the client's ID, IP address, port, state, and other attributes. It's typically used for monitoring, debugging, and managing client connections.

## Syntax

```plaintext
CLIENT LIST
```

## Parameter Explanations

`CLIENT LIST` does not require any parameters. When executed, it returns a list of connected clients with detailed information.

## Return Values

The command returns a single string with each line representing a connected client and its attributes. Each attribute is separated by a space. For example:

```plaintext
id=3 addr=127.0.0.1:6379 fd=7 name= age=144 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=32768 obl=0 oll=0 omem=0 events=r cmd=client
id=4 addr=192.168.1.2:6379 fd=8 name=myapp age=742 idle=10 flags=N db=1 sub=1 psub=0 multi=-1 qbuf=26 qbuf-free=32742 obl=0 oll=0 omem=0 events=r cmd=subscribe
```

## Code Examples

```cli
dragonfly> CLIENT LIST
"id=3 addr=127.0.0.1:6379 fd=7 name= age=144 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=32768 obl=0 oll=0 omem=0 events=r cmd=client
id=4 addr=192.168.1.2:6379 fd=8 name=myapp age=742 idle=10 flags=N db=1 sub=1 psub=0 multi=-1 qbuf=26 qbuf-free=32742 obl=0 oll=0 omem=0 events=r cmd=subscribe"
```

## Best Practices

- Regularly monitor the output of `CLIENT LIST` to understand the state of your clients and troubleshoot issues.
- Parse the output programmatically if you need to automate monitoring or logging.

## Common Mistakes

### Assuming the Command Requires Parameters

`CLIENT LIST` does not take any parameters, so avoid trying to provide arguments.

### Misinterpreting Output

The output is a single string with multiple lines, each representing a different client. Ensure you correctly parse each line and its properties.

## FAQs

### How can I filter specific clients using `CLIENT LIST`?

`CLIENT LIST` itself does not support filtering. You'll need to parse the output and apply your own filtering logic based on the client attributes.

### Can I get real-time updates from `CLIENT LIST`?

No, `CLIENT LIST` provides a snapshot at the moment it is called. For real-time monitoring, consider using `MONITOR` or integrating with Redis' Pub/Sub features.
