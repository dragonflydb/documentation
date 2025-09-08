---
description: Get to know about the Redis JSON.ARRTRIM command to trim an array to a specified range.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRTRIM

<PageTitle title="Redis JSON.ARRTRIM Command (Documentation) | Dragonfly" />

## Syntax

    JSON.ARRTRIM key path start stop

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Trim an array so that it contains only the specified inclusive range of elements

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`.
</details>

<details open><summary><code>start</code></summary> 

is index of the first element to keep (previous elements are trimmed). Default is 0. 
</details>

<details open><summary><code>stop</code></summary> 

is the index of the last element to keep (following elements are trimmed), including the last element. Default is 0. Negative values are interpreted as starting from the end.
</details>

:::note About out-of-range indexes


JSON.ARRTRIM is extremely forgiving, and using it with out-of-range indexes does not produce an error. Note a few differences between how RedisJSON v2.0 and legacy versions handle out-of-range indexes.

Behavior as of RedisJSON v2.0:

* If `start` is larger than the array's size or `start` > `stop`, returns 0 and an empty array. 
* If `start` is < 0, then start from the end of the array.
* If `stop` is larger than the end of the array, it is treated like the last element.

:::

## Return

JSON.ARRTRIM returns an array of integer replies for each path, the array's new size, or `nil`, if the matching JSON value is not an array.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec). 

## Examples

<details open>
<summary><b>Trim an array to a specific set of values</b></summary>

Create two headphone products with maximum sound levels.

``` bash
dragonfly> JSON.SET key $
"[[{\"name\":\"Healthy headphones\",\"description\":\"Wireless Bluetooth headphones with noise-cancelling technology\",\"connection\":{\"wireless\":true,\"type\":\"Bluetooth\"},\"price\":99.98,\"stock\":25,\"colors\":[\"black\",\"silver\"],\"max_level\":[60,70,80]},{\"name\":\"Noisy headphones\",\"description\":\"Wireless Bluetooth headphones with noise-cancelling technology\",\"connection\":{\"wireless\":true,\"type\":\"Bluetooth\"},\"price\":99.98,\"stock\":25,\"colors\":[\"black\",\"silver\"],\"max_level\":[85,90,100,120]}]]"
OK
```

Add new sound level values to the second product.

``` bash
dragonfly> JSON.ARRAPPEND key $[1].max_level 140 160 180 200 220 240 260 280
1) (integer) 12
```

Get the updated array.

``` bash
dragonfly> JSON.GET key $[1].max_level
"[[85,90,100,120,140,160,180,200,220,240,260,280]]"
```

Keep only the values between the fifth and the ninth element, inclusive of that last element.

``` bash
dragonfly> JSON.ARRTRIM key $[1].max_level 4 8
1) (integer) 5
```

Get the updated array.

``` bash
dragonfly> JSON.GET key $[1].max_level
"[[140,160,180,200,220]]"
```
</details>

## See also

`JSON.ARRINDEX` | `JSON.ARRINSERT`
