---
description: Reports the size in bytes of a key
---

# JSON.DEBUG MEMORY

## Syntax

    JSON.DEBUG MEMORY key [path]

**Time complexity:** O(N) when path is evaluated to a single value, where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key

Report a value's memory usage in bytes 

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. 
</details>

## Return

JSON.DEBUG MEMORY returns an integer reply specified as the value size in bytes.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec).

## Examples

<details open>
<summary><b>Report a value's memory usage in bytes</b></summary>

Create a JSON document.

``` bash
127.0.0.1:6379> JSON.SET item:2 $ '{"name":"Wireless earbuds","description":"Wireless Bluetooth in-ear headphones","connection":{"wireless":true,"type":"Bluetooth"},"price":64.99,"stock":17,"colors":["black","white"], "max_level":[80, 100, 120]}'
OK
```

Get the values' memory usage in bytes.

``` bash
127.0.0.1:6379> JSON.DEBUG MEMORY item:2
(integer) 253
```
</details>

## See also

`JSON.SET` | `JSON.ARRLEN` 

## Related topics

* [RedisJSON](https://redis.io/docs/stack/json)
* [Index and search JSON documents](https://redis.io/docs/stack/search/indexing_json)

