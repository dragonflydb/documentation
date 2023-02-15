---
description: Clear all entries from the slow log
---

# SLOWLOG RESET

## Syntax

    SLOWLOG RESET 

**Time complexity:** O(N) where N is the number of entries in the slowlog

This command resets the slow log, clearing all entries in it.

Once deleted the information is lost forever.

@reply

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK`
