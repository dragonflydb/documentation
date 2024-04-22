---
description: "Learn how to use Redis HRANDFIELD command to get one or more random fields from a hash. Add randomness in your data fetching."
---

import PageTitle from '@site/src/components/PageTitle';

# HRANDFIELD

<PageTitle title="Redis HRANDFIELD Command (Documentation) | Dragonfly" />

## Syntax

    HRANDFIELD key

**Time complexity:** O(N) where N is the number of fields returned

**ACL categories:** @read, @hash, @slow

When called with just the `key` argument, return a random field from the hash value stored at `key`.

If the provided `count` argument is positive, return an array of **distinct fields**.
The array's length is either `count` or the hash's number of fields (`HLEN`), whichever is lower.

If called with a negative `count`, the behavior changes and the command is allowed to return the **same field multiple times**.
In this case, the number of returned fields is the absolute value of the specified `count`.

The optional `WITHVALUES` modifier changes the reply so it includes the respective values of the randomly selected hash fields.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): without the additional `count` argument, the command returns a Bulk Reply with the randomly selected field, or `nil` when `key` does not exist.

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): when the additional `count` argument is passed, the command returns an array of fields, or an empty array when `key` does not exist.
If the `WITHVALUES` modifier is used, the reply is a list fields and their values from the hash.

## Examples

```shell
dragonfly> HMSET coin heads obverse tails reverse edge null
OK
dragonfly> HRANDFIELD coin
"heads"
dragonfly> HRANDFIELD coin
"tails"
dragonfly> HRANDFIELD coin -5 WITHVALUES
1) "edge"
2) "null"
3) "tails"
4) "reverse"
5) "heads"
6) "obverse"
7) "edge"
8) "null"
9) "heads"
10) "obverse"
```

## Specification of the behavior when count is passed

When the `count` argument is a positive value this command behaves as follows:

- No repeated fields are returned.
- If `count` is bigger than the number of fields in the hash, the command will only return the whole hash without additional fields.
- The order of fields in the reply is not truly random, so it is up to the client to shuffle them if needed.

When the `count` is a negative value, the behavior changes as follows:

- Repeating fields are possible.
- Exactly `count` fields, or an empty array if the hash is empty (non-existing key), are always returned.
- The order of fields in the reply is truly random.
