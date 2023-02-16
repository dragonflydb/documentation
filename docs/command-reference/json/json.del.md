---
description: Deletes a value
---

# JSON.DEL

## Syntax

    JSON.DEL key [path]

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the deleted value, O(N) when path is evaluated to multiple values, where N is the size of the key

Delete a value

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. Nonexisting paths are ignored.

:::note Note

 
Deleting an object's root is equivalent to deleting the key from Redis.


:::
</details>

## Return

JSON.DEL returns an integer reply specified as the number of paths deleted (0 or more).
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec).

## Examples

<details open>
<summary><b>Delete a value</b></summary>

Create a JSON document.

``` bash
127.0.0.1:6379> JSON.SET doc $ '{"a": 1, "nested": {"a": 2, "b": 3}}'
OK
```

Delete specified values.

``` bash
127.0.0.1:6379> JSON.DEL doc $..a
(integer) 2
```

Get the updated document.

``` bash
127.0.0.1:6379> JSON.GET doc $
"[{\"nested\":{\"b\":3}}]"
```
</details>

## See also

`JSON.SET` | `JSON.ARRLEN` 

## Related topics

* [RedisJSON](https://redis.io/docs/stack/json)
* [Index and search JSON documents](https://redis.io/docs/stack/search/indexing_json)



