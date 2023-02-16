---
description: Removes and returns the element at the specified index in the array at path
---

# JSON.ARRPOP

## Syntax

    JSON.ARRPOP key [path [index]]

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the array and the specified index is not the last element, O(1) when path is evaluated to a single value and the specified index is the last element, or O(N) when path is evaluated to multiple values, where N is the size of the key

Remove and return an element from the index in the array

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.
</details>

<details open><summary><code>index</code></summary> 

is position in the array to start popping from. Default is `-1`, meaning the last element. Out-of-range indexes round to their respective array ends. Popping an empty array returns null.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`.
</details>

## Return

`JSON.ARRPOP` returns an [array](https://redis.io/docs/reference/protocol-spec/#resp-arrays) of bulk string replies for each path, each reply is the popped JSON value, or `nil`, if the matching JSON value is not an array.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec). 

## Examples

<details open>
<summary><b>Pop a value from an index and insert a new value</b></summary>

Create two headphone products with maximum sound levels.

``` bash
127.0.0.1:6379> JSON.SET key $ '[{"name":"Healthy headphones","description":"Wireless Bluetooth headphones with noise-cancelling technology","connection":{"wireless":true,"type":"Bluetooth"},"price":99.98,"stock":25,"colors":["black","silver"],"max_level":[60,70,80]},{"name":"Noisy headphones","description":"Wireless Bluetooth headphones with noise-cancelling technology","connection":{"wireless":true,"type":"Bluetooth"},"price":99.98,"stock":25,"colors":["black","silver"],"max_level":[80,90,100,120]}]'
OK
```

Get all maximum values for the second product.

``` bash
127.0.0.1:6379> JSON.GET key $.[1].max_level
"[[80,90,100,120]]"
```

Update the `max_level` field of the product: remove an unavailable value and add a newly available value.

``` bash
127.0.0.1:6379> JSON.ARRPOP key $.[1].max_level 0
1) "80"
```

Get the updated array.

``` bash
127.0.0.1:6379> JSON.GET key $.[1].max_level
"[[90,100,120]]"
```

Now insert a new lowest value.

``` bash
127.0.0.1:6379> JSON.ARRINSERT key $.[1].max_level 0 85
1) (integer) 4
```

Get the updated array.

``` bash
127.0.0.1:6379> JSON.GET key $.[1].max_level
"[[85,90,100,120]]"
```
</details>

## See also

`JSON.ARRAPPEND` | `JSON.ARRINDEX` 

## Related topics

* [RedisJSON](https://redis.io/docs/stack/json)
* [Index and search JSON documents](https://redis.io/docs/stack/search/indexing_json)
