---
description: Find all keys matching the given pattern
---

# KEYS

## Syntax

    KEYS pattern

**Time complexity:** O(N) with N being the number of keys in the database, under the assumption that the key names in the database and the given pattern have limited length.

Returns all keys matching `pattern`.

While the time complexity for this operation is O(N), the constant times are
fairly low.

Supported glob-style patterns:

* `h?llo` matches `hello`, `hallo` and `hxllo`
* `h*llo` matches `hllo` and `heeeello`
* `h[ae]llo` matches `hello` and `hallo,` but not `hillo`
* `h[^e]llo` matches `hallo`, `hbllo`, ... but not `hello`
* `h[a-b]llo` matches `hallo` and `hbllo`

Use `\` to escape special characters if you want to match them verbatim.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of keys matching `pattern`.

**Number of elements returned:**
 
 Dragonfly protects itself from an overwhelming number of returned keys by imposing a limit on the quantity. To modify this limit, update the value of the "keys_output_limit" flag. Please refer to [Dragonfly configuration](https://github.com/dragonflydb/dragonfly#configuration) for more information how to change dragonfly flag values.

## Examples

```shell
dragonfly> MSET firstname Jack lastname Stuntman age 35
"OK"
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
