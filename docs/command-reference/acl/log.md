---
description: Print the ACL logs
---

import PageTitle from '@site/src/components/PageTitle';

# ACL LOG

<PageTitle title="Redis ACL LOG Explained (Better Than Official Docs)" />

"## Introduction and Use Case(s)

`ACL LOG` is a Redis command used to retrieve the Access Control List (ACL) logs. These logs provide information on recent ACL events, such as failed authentication attempts or unauthorized command executions. This command is useful for monitoring security-related activities within your Redis instance.

## Syntax

```plaintext
ACL LOG [<count>]
```

## Parameter Explanations

- `<count>`: Optional. An integer that specifies the number of log entries to return. If not provided, the default behavior is to return the latest 10 entries.

## Return Values

The command returns an array of log entries, each entry containing several fields:

- `count`: Total count of entries returned.
- `reason`: The reason for the log entry (e.g., `authentication`, `command`).
- `context`: Context in which the event occurred.
- `object`: The object involved in the log entry.
- `username`: The username associated with the event.
- `age-seconds`: Age of the log entry in seconds.
- `client-info`: Information about the client that triggered the event.

Example output:

```plaintext
1)  1) "count"
    2) "1"
    3) "reason"
    4) "command"
    5) "context"
    6) "toplevel"
    7) "object"
    8) "get"
    9) "username"
   10) "default"
   11) "age-seconds"
   12) "5"
   13) "client-info"
   14) "id=2 addr=127.0.0.1:6379 fd=6 name= age=5 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=26 qbuf-free=1024 obl=0 oll=0 omem=0 events=r cmd=get"
```

## Code Examples

```cli
dragonfly> ACL LOG
1)  1) "count"
    2) "1"
    3) "reason"
    4) "command"
    5) "context"
    6) "toplevel"
    7) "object"
    8) "get"
    9) "username"
   10) "default"
   11) "age-seconds"
   12) "5"
   13) "client-info"
   14) "id=2 addr=127.0.0.1:6379 fd=6 name= age=5 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=26 qbuf-free=1024 obl=0 oll=0 omem=0 events=r cmd=get"

dragonfly> ACL LOG 5
1) 1) "count"
   2) "5"
   ...
```

## Best Practices

- Regularly monitor `ACL LOG` to detect unusual activity early.
- Use automated scripts to alert you based on specific patterns in the logs.

## Common Mistakes

- Forgetting to specify the `<count>` parameter if more than 10 entries are needed.

### How can I clear the ACL logs?

You can clear the ACL logs using the `ACL LOG RESET` command.

### Can I limit the types of events logged by ACL?

No, `ACL LOG` records all relevant ACL-related events without filtering options.
