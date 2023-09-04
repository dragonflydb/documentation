---
description: Returns the JSON keys of the object at path
---

# JSON.OBJKEYS

## Syntax

    JSON.OBJKEYS key [path]

**Time complexity:** O(N) when path is evaluated to a single value, where N is the number of keys in the object, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Return the keys in the object that's referenced by `path`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse. Returns `null` for nonexistent keys.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. Returns `null` for nonexistant path.

</details>

## Return

JSON.OBJKEYS returns an array of array replies for each path, an array of the key names in the object as a bulk string reply, or `nil` if the matching JSON value is not an object. 
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec).

## Examples

``` bash
dragonfly> JSON.SET doc $ '{"a":[3], "nested": {"a": {"b":2, "c": 1}}}'
OK
dragonfly> JSON.OBJKEYS doc $..a
1) (nil)
2) 1) "b"
   2) "c"
```

## See also

`JSON.ARRINDEX` | `JSON.ARRINSERT` 
