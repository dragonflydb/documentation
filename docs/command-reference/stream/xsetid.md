---
description: Learn how to use Redis XSETID to set the last delivered ID for streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XSETID

<PageTitle title="Redis XSETID Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XSETID` command in Redis is used to set the stream's last entry ID. This can be useful for maintaining accurate stream sequences, especially after restoring data from backups or performing other administrative tasks.

## Syntax

```plaintext
XSETID <stream> <id>
```

## Parameter Explanations

- `<stream>`: The name of the stream for which you want to set the last entry ID.
- `<id>`: The ID to set as the last entry ID of the stream. The format should be like an existing entry ID, typically a millisecond-timestamp followed by a sequence number (e.g., `1659470001234-0`).

## Return Values

`OK` if the command was successful.

### Examples:

- Success: `"OK"`
- Error: `(error) ERR no such key` if the stream does not exist.

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1659470001234-0"
dragonfly> XSETID mystream 1659470001245-0
OK
dragonfly> XINFO STREAM mystream
 1) "length"
 2) (integer) 1
 3) "last-generated-id"
 4) "1659470001245-0"
 5) "entries"
 6) 1) 1) "1659470001234-0"
       2) 1) "field1"
          2) "value1"
```

## Best Practices

- Ensure the ID you're setting with `XSETID` is logically consistent with the stream's existing IDs to avoid confusion or potential data integrity issues.
- Use `XINFO STREAM <stream>` to inspect the current state of your stream before and after using `XSETID`.

## Common Mistakes

- Setting an ID that already exists in the stream may cause unexpected behavior in future stream operations. Always ensure the new ID is unique within the context of the stream.
- Attempting to set an ID on a non-existing stream will result in an error. Make sure the stream exists before using `XSETID`.

## FAQs

### What happens if I set an ID that is lower than existing IDs in the stream?

This can lead to unexpected behavior in subsequent stream operations, as the command doesn't re-order or remove existing entries. It simply sets the internal last generated ID marker.

### Is there a way to revert the ID set by `XSETID`?

No direct command to revert `XSETID` is available. You would need to carefully manage and possibly restore the stream to a known good state from backup or other means.

### Can I use `XSETID` to reset a stream to start from zero?

In theory, yes, but it’s not recommended unless you are fully aware of the implications on downstream consumers and the integrity of the stream history.
