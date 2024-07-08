---
description: Learn how to use Redis LASTSAVE command to obtain the UNIX timestamp of the last database save.
---

import PageTitle from '@site/src/components/PageTitle';

# LASTSAVE

<PageTitle title="Redis LASTSAVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LASTSAVE` command is used to fetch the Unix timestamp of the last successful Redis database save operation. This is particularly useful for monitoring and debugging purposes to ensure that your data has been persisted correctly.

## Syntax

```plaintext
LASTSAVE
```

## Parameter Explanations

The `LASTSAVE` command does not take any parameters. It simply returns the timestamp of the last successful save.

## Return Values

The `LASTSAVE` command returns an integer representing the Unix timestamp of the last successful save operation.

### Example:

If the last successful save happened on July 8, 2024, at 12:34:56 PM UTC, the `LASTSAVE` command will return the corresponding Unix timestamp:

```cli
dragonfly> LASTSAVE
(integer) 1657289696
```

## Code Examples

```cli
dragonfly> LASTSAVE
(integer) 1657289696
```

## Best Practices

- Regularly monitor the output of `LASTSAVE` to keep track of when your data was last saved.
- Combine `LASTSAVE` with other commands like `BGSAVE` or `SAVE` to programmatically ensure data persistence in backup routines.

## Common Mistakes

- Misinterpreting the returned integer as a direct date-time value. It needs to be converted from a Unix timestamp to a human-readable format.
- Assuming `LASTSAVE` triggers a save operation; it only returns the timestamp of the last save.

## FAQs

### What happens if no save has ever occurred?

If no successful save operation has been performed yet, `LASTSAVE` will return a Unix timestamp of 0, which corresponds to 1970-01-01 00:00:00 UTC.

### Can `LASTSAVE` be used to trigger a save?

No, `LASTSAVE` cannot trigger a save operation. It only retrieves the timestamp of the last save. To trigger a save, use `SAVE` or `BGSAVE`.
