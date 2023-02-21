---
description: Get the UNIX time stamp of the last successful save to disk
---

# LASTSAVE

## Syntax

    LASTSAVE 

**Time complexity:** O(1)

Return the UNIX TIME of the last DB save executed with success.
A client may check if a `BGSAVE` command succeeded reading the `LASTSAVE` value,
then issuing a `BGSAVE` command and checking at regular intervals every N
seconds if `LASTSAVE` changed. Dragonfly considers the database saved successfully at startup.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): an UNIX time stamp.
