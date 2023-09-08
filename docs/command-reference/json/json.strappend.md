---
description: Appends a string to a JSON string value at path
---

# JSON.STRAPPEND

## Syntax

    JSON.STRAPPEND key [path] value

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Append the `json-string` values to the string at `path`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.
</details>

<details open><summary><code>value</code></summary> 

is value to append to one or more strings. 

:::note About using strings with JSON commands

To specify a string as an array value to append, wrap the quoted string with an additional set of single quotes. Example: `'"silver"'`. For more detailed use, see [Examples](#examples).

:::
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`.
</details>

## Return value 

JSON.STRAPPEND returns an array of integer replies for each path, the string's new length, or `nil`, if the matching JSON value is not a string.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec). 

## Examples

``` bash
dragonfly> JSON.SET doc $ '{"a":"foo", "nested": {"a": "hello"}, "nested2": {"a": 31}}'
OK
dragonfly> JSON.STRAPPEND doc $..a '"baz"'
1) (integer) 6
2) (integer) 8
3) (nil)
dragonfly> JSON.GET doc $
"[{\"a\":\"foobaz\",\"nested\":{\"a\":\"hellobaz\"},\"nested2\":{\"a\":31}}]"
```

## See also

`JSON.ARRAPEND` | `JSON.ARRINSERT` 

## Related topics

* [RedisJSON](https://redis.io/docs/stack/json)
* [Index and search JSON documents](https://redis.io/docs/stack/search/indexing_json)

