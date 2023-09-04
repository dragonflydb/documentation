---
description: Clears all values from an array or an object and sets numeric values to `0`
---

# JSON.CLEAR

## Syntax

    JSON.CLEAR key [path]

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the values, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Clear container values (arrays/objects) and set numeric values to `0`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. Nonexisting paths are ignored.
</details>

## Return

JSON.CLEAR returns an integer reply specified as the number of values cleared. 
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec).

:::note Note

 
Already cleared values are ignored for empty containers and zero numbers.


:::

## Examples

<details open>
<summary><b>Clear container values and set numeric values to <code>0</code></b></summary>

Create a JSON document.

``` bash
dragonfly> JSON.SET doc $ '{"obj":{"a":1, "b":2}, "arr":[1,2,3], "str": "foo", "bool": true, "int": 42, "float": 3.14}'
OK
```

Clear all container values. This returns the number of objects with cleared values.

``` bash
dragonfly> JSON.CLEAR doc $.*
(integer) 4
```

Get the updated document. Note that numeric values have been set to `0`.

``` bash
dragonfly> JSON.GET doc $
"[{\"obj\":{},\"arr\":[],\"str\":\"foo\",\"bool\":true,\"int\":0,\"float\":0}]"
```
</details>

## See also

`JSON.ARRINDEX` | `JSON.ARRINSERT` 

