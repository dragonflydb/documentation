---
description: "Learn to use Redis KEYS command to find keys that match a pattern."
---

import PageTitle from '@site/src/components/PageTitle';

# KEYS

<PageTitle title="Redis KEYS Command (Documentation) | Dragonfly" />

## Syntax

    KEYS pattern

**Time complexity:** O(N) with N being the number of keys in the database, under the assumption that the key names in the database and the given pattern have limited length.

**ACL categories:** @keyspace, @read, @slow, @dangerous

Returns all keys matching `pattern`.
While the time complexity for this operation is O(N), the constant times are fairly low.

Supported glob-style patterns:

- `h?llo` matches `hello`, `hallo` and `hxllo`
- `h*llo` matches `hllo` and `heeeello`
- `h[ae]llo` matches `hello` and `hallo,` but not `hillo`
- `h[^e]llo` matches `hallo`, `hbllo`, ... but not `hello`
- `h[a-b]llo` matches `hallo` and `hbllo`

Use `\` to escape special characters if you want to match them verbatim.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): list of keys matching `pattern`.

### Number of Elements Returned

Dragonfly protects itself from an overwhelming number of returned keys by imposing a limit on the quantity.
To modify this limit, update the value of the [`--keys_output_limit`](../../managing-dragonfly/flags.md#--keys_output_limit) server configuration flag.

## Examples

```shell
dragonfly> MSET firstname Jack lastname Stuntman age 35
OK
dragonfly> KEYS *name*
1) "lastname"
2) "firstname"
dragonfly> KEYS a??
1) "age"
dragonfly> KEYS *
1) "lastname"
2) "age"
3) "firstname"
```
