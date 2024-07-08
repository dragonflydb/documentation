---
description: Learn how to use Redis XGROUP SETID to set the last delivered ID of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP SETID

<PageTitle title="Redis XGROUP SETID Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XGROUP SETID` is a Redis command used to set the next message ID that a consumer group will read from a stream. This is useful for managing message consumption in distributed systems, ensuring consumers can reset or reinitialize their position within a stream.

## Syntax

```plaintext
XGROUP SETID <key> <groupname> <id>
```

## Parameter Explanations

- `<key>`: The name of the stream.
- `<groupname>`: The name of the consumer group whose ID you want to set.
- `<id>`: The message ID to set as the next one for the consumer group to read. It can be a specific ID (e.g., `0-1`), `$` to start from the new messages, or any other valid stream ID format.

## Return Values

Returns `OK` upon successful execution.

### Examples of possible outputs:

- `(error) NOGROUP No such key 'mystream' or consumer group 'mygroup'` if the stream or group doesn't exist.
- `OK` if the operation is successful.

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1688463669190-0"
dragonfly> XGROUP CREATE mystream mygroup 0
OK
dragonfly> XGROUP SETID mystream mygroup $
OK
dragonfly> XREADGROUP GROUP mygroup myconsumer COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) "1688463669190-0"
      2) 1) "field1"
         2) "value1"
dragonfly> XGROUP SETID mystream mygroup 0
OK
dragonfly> XREADGROUP GROUP mygroup myconsumer COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) "1688463669190-0"
      2) 1) "field1"
         2) "value1"
```

## Best Practices

- Ensure the stream and consumer group exist before using `XGROUP SETID`.
- Use `$` carefully; it sets the consumer group to read only new messages, potentially skipping unprocessed ones.

## Common Mistakes

- Trying to set an ID on a non-existent stream or consumer group.
- Misunderstanding the `$` parameter, which can lead to missing out on pending messages if not used appropriately.

## FAQs

### What happens if I use XGROUP SETID with an invalid ID?

Redis will return an error indicating the issue with the provided ID. Always ensure the ID follows the correct stream ID format.
