---
description: Returns the length of the JSON String at path in key
---

# JSON.STRLEN

## Syntax

    JSON.STRLEN key [path]

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Report the length of the JSON String at `path` in `key`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`, if not provided. Returns null if the `key` or `path` do not exist.
</details>

## Return

JSON.STRLEN returns by recursive descent an array of integer replies for each path, the array's length, or `nil`, if the matching JSON value is not a string.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec). 

## Examples

``` bash
dragonfly> JSON.SET doc $ '{"a":"foo", "nested": {"a": "hello"}, "nested2": {"a": 31}}'
OK
dragonfly> JSON.STRLEN doc $..a
1) (integer) 3
2) (integer) 5
3) (nil)
```

## See also

`JSON.ARRLEN` | `JSON.ARRINSERT` 
