---
description:  Learn how to use Redis XDEL to delete a message from a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XDEL

<PageTitle title="Redis XDEL Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XDEL` command is used to delete one or more entries from a stream.
This command is particularly useful for managing data in stream-like structures by removing irrelevant or processed items.

## Syntax

```shell
XDEL key ID [ID ...]
```

## Parameter Explanations

- `key`: The key of the stream from which entries are to be deleted.
- `ID`: One or more entry IDs identifying the entries you wish to delete from the stream.

## Return Values

The command returns an integer representing the number of entries that were successfully deleted from the stream.

## Code Examples

### Basic Example

Delete a single entry from a stream:

```shell
dragonfly> XADD mystream * name "Alice" age "30"
"1527845627383-0"
dragonfly> XADD mystream * name "Bob" age "25"
"1527845627383-1"
dragonfly> XDEL mystream 1527845627383-0
(integer) 1
dragonfly> XRANGE mystream -
1) 1527845627383-1
   1) "name"
   2) "Bob"
   3) "age"
   4) "25"
```

### Delete Multiple Entries

Delete multiple entries from the stream by specifying multiple IDs:

```shell
dragonfly> XADD mystream * name "Charlie" age "22"
"1527845627383-2"
dragonfly> XADD mystream * name "Diana" age "28"
"1527845627383-3"
dragonfly> XDEL mystream 1527845627383-1 1527845627383-3
(integer) 2
dragonfly> XRANGE mystream -
1) 1527845627383-2
   1) "name"
   2) "Charlie"
   3) "age"
   4) "22"
```

## Best Practices

- Make smart use of `XDEL` to keep your streams tidy and free from outdated or unnecessary data.
- Consider removing processed entries to prevent the stream from growing indefinitely, which could lead to performance degradation.

## Common Mistakes

- Attempting to delete an entry using a non-existent ID, which will result in a deletion count of `0`.
- Assuming `XDEL` modifies the stream's order, while it merely removes specific entries and maintains the order of remaining entries.

## FAQs

### What happens if the specified IDs do not exist in the stream?

If the specified IDs do not exist, `XDEL` will return `0` for each non-existent ID, meaning no entries were deleted.

### Can I use `XDEL` on a non-stream data type?

No, using `XDEL` on a non-stream data type will result in an error, as this command is specifically designed for stream entries.