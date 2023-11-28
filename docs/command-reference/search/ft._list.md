---
description: Returns a list of all existing indexes
---

# FT._LIST

## Syntax

    FT._LIST 

**Time complexity:** O(1)

Returns a list of all existing indexes.


{{% alert title="Temporary command" color="info" %}}
The prefix `_` in the command indicates, this is a temporary command.

In the future, a `SCAN` type of command will be added, for use when a database
contains a large number of indices.

:::

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays) with index names.

## Examples

```sql
FT._LIST
1) "idx"
2) "movies"
3) "imdb"
```