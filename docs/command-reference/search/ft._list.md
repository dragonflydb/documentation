---
description: Returns a list of all existing indexes
---

import PageTitle from '@site/src/components/PageTitle';

# FT.\_LIST

<PageTitle title="Redis FT._LIST Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `FT._LIST` command in Redis is used to list all the indexes currently defined in the RediSearch module. This command is especially useful for monitoring and managing the various search indexes, which can be critical in applications that rely on full-text search capabilities.

## Syntax

```
FT._LIST
```

## Parameter Explanations

The `FT._LIST` command does not accept any parameters. It simply lists all existing indexes.

## Return Values

The command returns an array of strings, each representing the name of an index. If no indexes are defined, an empty array is returned.

Example outputs:

- If there are three indexes: `["index1", "index2", "index3"]`
- If there are no indexes: `[]`

## Code Examples

```cli
dragonfly> FT.CREATE myIndex ON HASH PREFIX 1 doc: SCHEMA title TEXT WEIGHT 5.0 body TEXT
OK
dragonfly> FT.CREATE anotherIndex ON HASH PREFIX 1 item: SCHEMA name TEXT WEIGHT 1.0 description TEXT
OK
dragonfly> FT._LIST
1) "myIndex"
2) "anotherIndex"
```

## Best Practices

- Regularly use `FT._LIST` to monitor active indexes, helping you ensure that your search infrastructure is organized and efficient.
- Combine this command with other management commands like `FT.INFO` to get detailed information about each index.

## Common Mistakes

- Attempting to pass parameters to `FT._LIST`. This command does not take any arguments and will return an error if used incorrectly.

## FAQs

### What happens if there are no indexes?

If there are no indexes defined, `FT._LIST` will return an empty array.

### Can I use patterns or filters with `FT._LIST`?

No, `FT._LIST` simply lists all indexes without filtering. For specific details about an index, use `FT.INFO`.
