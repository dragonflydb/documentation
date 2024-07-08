---
description: Learn how to use Redis XDEL to delete a message from a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XDEL

<PageTitle title="Redis XDEL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XDEL` is a command in Redis used to delete entries from a stream. This is useful in scenarios where you need to remove specific messages from a stream, such as purging outdated or irrelevant data.

## Syntax

```plaintext
XDEL key ID [ID ...]
```

## Parameter Explanations

- **key**: The name of the stream from which you want to delete entries.
- **ID**: One or more entry IDs that specify which entries to delete from the stream.

## Return Values

The `XDEL` command returns an integer representing the number of entries that were successfully removed.

### Example

If you delete one entry:

```cli
(integer) 1
```

If none of the specified entries exist:

```cli
(integer) 0
```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1627812000000-0"
dragonfly> XADD mystream * field2 value2
"1627812001000-0"
dragonfly> XLEN mystream
(integer) 2
dragonfly> XDEL mystream 1627812000000-0
(integer) 1
dragonfly> XLEN mystream
(integer) 1
dragonfly> XRANGE mystream - +
1) "1627812001000-0"
   1) "field2"
   2) "value2"
```

## Best Practices

- Ensure the entry ID exists before attempting to delete it.
- Use `XLEN` to check the number of entries before and after deletion to confirm the operation's success.

## Common Mistakes

- Trying to delete non-existent entry IDs will result in a return value of 0.
- Deleting all entries this way doesn't delete the stream itself; use `DEL` for that purpose.

## FAQs

### Does `XDEL` remove the stream if all entries are deleted?

No, `XDEL` only removes the specified entries. To remove the stream, use the `DEL` command.

### Can I delete multiple entries at once with `XDEL`?

Yes, you can specify multiple entry IDs in a single `XDEL` command to delete multiple entries simultaneously.
