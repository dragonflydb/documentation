---
description: Learn how to use Redis XSETID to set the last delivered ID for streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XSETID

<PageTitle title="Redis XSETID Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XSETID` is a Redis command used to change the ID of an existing stream. This can be useful in scenarios where you need to reset the ID sequence for a stream, often for replication or data recovery purposes.

## Syntax

```
XSETID <stream> <new_id>
```

## Parameter Explanations

- `<stream>`: The name of the stream whose ID you want to set.
- `<new_id>`: The new ID to set for the stream. This should be in the format `milliseconds-sequence`.

## Return Values

The command returns `OK` if the operation is successful.

## Code Examples

```cli
dragonfly> XADD mystream * name "Alice"
"1657899999999-0"
dragonfly> XADD mystream * name "Bob"
"1657900000000-0"
dragonfly> XLEN mystream
(integer) 2
dragonfly> XSETID mystream 1657900000000-1
OK
dragonfly> XLEN mystream
(integer) 2
dragonfly> XADD mystream * name "Charlie"
"1657900000000-2"
dragonfly> XRANGE mystream - +
1) 1) "1657899999999-0"
   2) 1) "name"
      2) "Alice"
2) 1) "1657900000000-0"
   2) 1) "name"
      2) "Bob"
3) 1) "1657900000000-2"
   2) 1) "name"
      2) "Charlie"
```

## Best Practices

- Ensure that the new ID is greater than the last ID in the stream to avoid conflicts.
- Use `XSETID` judiciously as improper use might lead to data consistency issues, especially in replicated environments.

## Common Mistakes

- Setting `<new_id>` to an ID that is less than or equal to the current maximum ID in the stream. This will cause subsequent additions to the stream to fail with an error.

## FAQs

### Can I use XSETID to decrease the ID sequence?

No, the new ID must always be greater than the current maximum ID in the stream to maintain the order of entries.

### What happens if I set an invalid ID format?

Redis will return an error indicating that the ID format is invalid. Ensure the ID follows the `milliseconds-sequence` format.
