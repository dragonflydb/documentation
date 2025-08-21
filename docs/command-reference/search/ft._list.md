---
description: Returns a list of all existing indexes
---

# FT._LIST

## Syntax

    FT._LIST 

**Time complexity:** O(1)

## Description

Return a list of all existing indexes.

The prefix `_` in the command indicates that this is a temporary command.
In the future, a `SCAN` type of command will be added for use when a database contains a large number of indices.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec#arrays) with index names.

## Examples

```bash
dragonfly> FT._LIST
1) "idx"
2) "movies"
3) "imdb"
```

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
