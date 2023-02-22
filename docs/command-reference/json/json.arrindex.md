---
description: Returns the index of the first occurrence of a JSON scalar value in
  the array at path
---

# JSON.ARRINDEX

## Syntax

    JSON.ARRINDEX key path value [start [stop]]

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key

Search for the first occurrence of a JSON value in an array

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse.
</details>

<details open><summary><code>value</code></summary> 

is value to find its index in one or more arrays. 

:::note About using strings with JSON commands

To specify a string as an array value to index, wrap the quoted string with an additional set of single quotes. Example: `'"silver"'`. For more detailed use, see [Examples](#examples).

:::
</details>

## Optional arguments

<details open><summary><code>start</code></summary> 

is inclusive start value to specify in a slice of the array to search. Default is `0`. 
</details>


<details open><summary><code>stop</code></summary> 

is exclusive stop value to specify in a slice of the array to search, including the last element. Default is `0`. Negative values are interpreted as starting from the end.
</details>

:::note About out-of-range indexes


Out-of-range indexes round to the array's start and end. An inverse index range (such as the range from 1 to 0) returns unfound or `-1`.

:::

## Return value 

`JSON.ARRINDEX` returns an [array](https://redis.io/docs/reference/protocol-spec/#resp-arrays) of integer replies for each path, the first position in the array of each JSON value that matches the path, `-1` if unfound in the array, or `nil`, if the matching JSON value is not an array.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec). 

## Examples

<details open>
<summary><b>Find the specific place of a color in a list of product colors</b></summary>

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
JSON.GET item:1
"{\"name\":\"Noise-cancelling Bluetooth headphones\",\"description\":\"Wireless Bluetooth headphones with noise-cancelling technology\",\"connection\":{\"wireless\":true,\"type\":\"Bluetooth\"},\"price\":99.98,\"stock\":25,\"colors\":[\"black\",\"silver\",\"blue\"]}"
```

Get the list of colors for the product.

``` bash
dragonfly> JSON.GET item:1 '$.colors[*]'
"[\"black\",\"silver\",\"blue\"]"
```

Insert two more colors after the second color. You now have five colors.

``` bash
dragonfly> JSON.ARRINSERT item:1 $.colors 2 '"yellow"' '"gold"'
1) (integer) 5
```

Get the updated list of colors.

``` bash
dragonfly> JSON.GET item:1 $.colors
"[[\"black\",\"silver\",\"yellow\",\"gold\",\"blue\"]]"
```

Find the place where color `silver` is located.

``` bash
dragonfly> JSON.ARRINDEX item:1 $..colors '"silver"'
1) (integer) 1
```
</details>

## See also

`JSON.ARRAPPEND` | `JSON.ARRINSERT` 

