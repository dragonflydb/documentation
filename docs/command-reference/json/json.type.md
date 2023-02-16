---
description: Returns the type of the JSON value at path
---

# JSON.TYPE

## Syntax

    JSON.TYPE key [path]

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

Report the type of JSON value at `path`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. Returns null if the `key` or `path` do not exist.

</details>

## Return

JSON.TYPE returns an array of string replies for each path, specified as the value's type.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec).

## Examples

``` bash
127.0.0.1:6379> JSON.SET doc $ '{"a":2, "nested": {"a": true}, "foo": "bar"}'
OK
127.0.0.1:6379> JSON.TYPE doc $..foo
1) "string"
127.0.0.1:6379> JSON.TYPE doc $..a
1) "integer"
2) "boolean"
127.0.0.1:6379> JSON.TYPE doc $..dummy
```

## See also

`JSON.SET` | `JSON.ARRLEN` 

## Related topics

* [RedisJSON](https://redis.io/docs/stack/json)
* [Index and search JSON documents](https://redis.io/docs/stack/search/indexing_json)



