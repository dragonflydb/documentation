---
description: Increments the numeric value at path by a value
---

# JSON.NUMINCRBY

## Syntax

    JSON.NUMINCRBY key path value

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

Increment the number value stored at `path` by `number`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.
</details>

<details open><summary><code>value</code></summary> 

is number value to increment. 
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`.
</details>

## Return 

JSON.NUMINCRBY returns a bulk string reply specified as a stringified new value for each path, or `nil`, if the matching JSON value is not a number. 
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec). 

## Examples

<details open>
<summary><b>Increment number values</b></summary>

Create a document.

``` bash
127.0.0.1:6379> JSON.SET doc . '{"a":"b","b":[{"a":2}, {"a":5}, {"a":"c"}]}'
OK
```

Increment a value of `a` object by 2. The command fails to find a number and returns `null`.

``` bash
127.0.0.1:6379> JSON.NUMINCRBY doc $.a 2
"[null]"
```

Recursively find and increment a value of all `a` objects. The command increments numbers it finds and returns `null` for nonnumber values.

``` bash
127.0.0.1:6379> JSON.NUMINCRBY doc $..a 2
"[null,4,7,null]"
```

</details>

## See also

`JSON.ARRINDEX` | `JSON.ARRINSERT` 

## Related topics

* [RedisJSON](https://redis.io/docs/stack/json)
* [Index and search JSON documents](https://redis.io/docs/stack/search/indexing_json)
