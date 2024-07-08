---
description: Learn how to use Redis XDEL to delete a message from a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XDEL

<PageTitle title="Redis XDEL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XDEL` command in Redis is used to remove one or more entries from a stream. This is particularly useful for managing stream sizes and ensuring that outdated or processed entries do not consume memory unnecessarily. Typical use cases include maintaining a fixed-size stream by periodically deleting old entries and removing specific entries after they have been processed.

## Syntax

```plaintext
XDEL key ID [ID ...]
```

## Parameter Explanations

- `key`: The name of the stream from which entries are to be deleted.
- `ID`: One or more stream entry IDs to be removed. Each ID uniquely identifies an entry within the stream.

## Return Values

The `XDEL` command returns an integer indicating the number of entries that were successfully removed from the stream.

Example return values:

- `(integer) 1`: One entry was successfully deleted.
- `(integer) 0`: No entries were found with the specified IDs, so none were deleted.

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1628847740145-0"
dragonfly> XADD mystream * field2 value2
"1628847741146-0"
dragonfly> XRANGE mystream -
1) "1628847740145-0"
   1) "field1"
   2) "value1"
2) "1628847741146-0"
   1) "field2"
   2) "value2"
dragonfly> XDEL mystream 1628847740145-0
(integer) 1
dragonfly> XRANGE mystream -
1) "1628847741146-0"
   1) "field2"
   2) "value2"
dragonfly> XDEL mystream 1628847749999-0
(integer) 0
```

## Best Practices

- Consider batch deleting entries if there are multiple IDs to remove, as this can be more efficient than issuing individual `XDEL` commands.
- Combine `XTRIM` and `XDEL` to manage stream size effectively, ensuring you do not exceed your memory constraints.

## Common Mistakes

- Deleting non-existent IDs: Ensure the IDs you wish to delete actually exist in the stream to avoid unnecessary operations.
- Confusing `XDEL` with `XTRIM`: `XDEL` removes specific entries by ID, while `XTRIM` trims the stream to a maximum length or minimum ID.

## FAQs

### Can `XDEL` remove multiple entries in a single command?

Yes, you can specify multiple IDs in a single `XDEL` command to delete several entries at once.

### What happens if I try to delete an entry that does not exist?

If you try to delete an entry with an ID that does not exist, `XDEL` will simply return `(integer) 0`, indicating no entries were deleted.
