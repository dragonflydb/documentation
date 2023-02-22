---
description: Toggles a boolean value
---

# JSON.TOGGLE

## Syntax

    JSON.TOGGLE key path

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

Toggle a Boolean value stored at `path`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.
</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. 

</details>

## Return

JSON.TOGGLE returns an array of integer replies for each path, the new value (`0` if `false` or `1` if `true`), or `nil` for JSON values matching the path that are not Boolean.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/reference/protocol-spec).

## Examples

<details open>
<summary><b>Toogle a Boolean value stored at <code>path</code></b></summary>

Create a JSON document.

``` bash
dragonfly> JSON.SET doc $ '{"bool": true}'
OK
```

Toggle the Boolean value.

``` bash
dragonfly> JSON.TOGGLE doc $.bool
1) (integer) 0
```

Get the updated document.

``` bash
dragonfly> JSON.GET doc $
"[{\"bool\":false}]"
```

Toggle the Boolean value.

``` bash
dragonfly> JSON.TOGGLE doc $.bool
1) (integer) 1
```

Get the updated document.

``` bash
dragonfly> JSON.GET doc $
"[{\"bool\":true}]"
```
</details>

## See also

`JSON.SET` | `JSON.GET` 
