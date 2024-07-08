---
description: Learn how to use Redis TIME command to fetch the current server time.
---

import PageTitle from '@site/src/components/PageTitle';

# TIME

<PageTitle title="Redis TIME Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `TIME` command in Redis returns the current server time as a Unix timestamp and microsecond precision. It is typically used for synchronizing operations, logging events with consistent timestamps, or generating unique IDs based on the server's current time.

## Syntax

```plaintext
TIME
```

## Parameter Explanations

The `TIME` command does not take any parameters.

## Return Values

The `TIME` command returns an array containing two strings:

1. The first string represents the Unix timestamp in seconds.
2. The second string represents the microseconds part of the time.

Example output:

```plaintext
1) "1625588827"
2) "123456"
```

## Code Examples

```cli
dragonfly> TIME
1) "1625588827"
2) "123456"
```

## Best Practices

- Use the `TIME` command when you need precise, current server time for logging or time-based calculations.
- Combine `TIME` with other commands to create time-stamped entries in your datasets.

## Common Mistakes

- Assuming the `TIME` command returns a single value instead of an array.
- Using `TIME` without considering the time zone of the server, which could lead to discrepancies if your application spans multiple time zones.

## FAQs

### How accurate is the time returned by the `TIME` command?

The `TIME` command provides the current server time with microsecond precision, making it highly accurate for most use cases.

### Can the `TIME` command be used for issuing timeouts or delays?

No, `TIME` only returns the server's current time. For issuing timeouts or delays, consider using commands like `PEXPIRE` or `SETEX`.
