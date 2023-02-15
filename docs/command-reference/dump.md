---
description: Return a serialized version of the value stored at the specified key.
---

# DUMP

## Syntax

    DUMP key

**Time complexity:** O(1) to access the key and additional O(N*M) to serialize it, where N is the number of Redis objects composing the value and M their average size. For small string values the time complexity is thus O(1)+O(1*M) where M is small, so simply O(1).

Serialize the value stored at key in a Redis-specific format and return it to
the user.
The returned value can be synthesized back into a Redis key using the `RESTORE`
command.

The serialization format is opaque and non-standard, however it has a few
semantic characteristics:

* It contains a 64-bit checksum that is used to make sure errors will be
  detected.
  The `RESTORE` command makes sure to check the checksum before synthesizing a
  key using the serialized value.
* Values are encoded in the same format used by RDB.
* An RDB version is encoded inside the serialized value, so that different Redis
  versions with incompatible RDB formats will refuse to process the serialized
  value.

The serialized value does NOT contain expire information.
In order to capture the time to live of the current value the `PTTL` command
should be used.

If `key` does not exist a nil bulk reply is returned.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the serialized value.

## Examples

```
> SET mykey 10
OK
> DUMP mykey
"\x00\xc0\n\n\x00n\x9fWE\x0e\xaec\xbb"
```
