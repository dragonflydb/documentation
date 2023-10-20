---
description: Understand how to use Redis JSON.ARRAPPEND command to append an element into a JSON array.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRAPPEND

<PageTitle title="Redis JSON.ARRAPPEND Command (Documentation) | Dragonfly" />

## Syntax

    JSON.ARRAPPEND key [path] value [value ...]

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Append the `json` values into the array at `path` after the last element in it

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.
</details>

<details open><summary><code>value</code></summary> 

is one or more values to append to one or more arrays. 

:::note About using strings with JSON commands

To specify a string as an array value to append, wrap the quoted string with an additional set of single quotes. Example: `'"silver"'`. For more detailed use, see [Examples](#examples).

:::
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`.
</details>

## Return value 

`JSON.ARRAPEND` returns an [array](https://redis.io/docs/reference/protocol-spec/#resp-arrays) of integer replies for each path, the array's new size, or `nil`, if the matching JSON value is not an array. 
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec). 

## Examples

<details open>
<summary><b>Add a new color to a list of product colors</b></summary>

Create a document for noise-cancelling headphones in black and silver colors.

``` bash
dragonfly> JSON.SET item:1 $ '{"name":"Noise-cancelling Bluetooth headphones","description":"Wireless Bluetooth headphones with noise-cancelling technology","connection":{"wireless":true,"type":"Bluetooth"},"price":99.98,"stock":25,"colors":["black","silver"]}'
OK
```

Add color `blue` to the end of the `colors` array. `JSON.ARRAPEND` returns the array's new size.

``` bash
dragonfly> JSON.ARRAPPEND item:1 $.colors '"blue"'
1) (integer) 3
```

Return the new length of the `colors` array.

``` bash
dragonfly> JSON.GET item:1
"{\"name\":\"Noise-cancelling Bluetooth headphones\",\"description\":\"Wireless Bluetooth headphones with noise-cancelling technology\",\"connection\":{\"wireless\":true,\"type\":\"Bluetooth\"},\"price\":99.98,\"stock\":25,\"colors\":[\"black\",\"silver\",\"blue\"]}"
```

</details>

## See also

`JSON.ARRINDEX` | `JSON.ARRINSERT` 
