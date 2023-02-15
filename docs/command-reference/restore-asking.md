---
description: An internal command for migrating keys in a cluster
---

# RESTORE-ASKING

## Syntax

    RESTORE-ASKING key ttl serialized-value [REPLACE] [ABSTTL] [IDLETIME seconds] [FREQ frequency]

**Time complexity:** O(1) to create the new key and additional O(N*M) to reconstruct the serialized value, where N is the number of Redis objects composing the value and M their average size. For small string values the time complexity is thus O(1)+O(1*M) where M is small, so simply O(1). However for sorted set values the complexity is O(N*M*log(N)) because inserting values into sorted sets is O(log(N)).

The `RESTORE-ASKING` command is an internal command.
It is used by a Redis cluster master during slot migration.