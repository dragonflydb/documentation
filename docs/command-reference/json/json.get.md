---
description: Learn using Redis JSON.GET command to retrieve a value from a JSON document.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.GET

<PageTitle title="Redis JSON.GET Command (Documentation) | Dragonfly" />

## Syntax

    JSON.GET key [INDENT indent] [NEWLINE newline] [SPACE space] [NOESCAPE] [paths [paths ...]]

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Return the value at `path` in JSON serialized form

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse.

</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. JSON.GET accepts multiple `path` arguments.

</details>

:::note Note


When using a single JSONPath, the root of the matching values is a JSON string with a top-level **array** of serialized JSON value. 
In contrast, a legacy path returns a single value.

When using multiple JSONPath arguments, the root of the matching values is a JSON string with a top-level **object**, with each object value being a top-level array of serialized JSON value.
In contrast, if all paths are legacy paths, each object value is a single serialized JSON value.
If there are multiple paths that include both legacy path and JSONPath, the returned value conforms to the JSONPath version (an array of values).


:::

<details open><summary><code>INDENT</code></summary> 

sets the indentation string for nested levels.

</details>

<details open><summary><code>NEWLINE</code></summary> 

sets the string that's printed at the end of each line.

</details>

<details open><summary><code>SPACE</code></summary> 

sets the string that's put between a key and a value.

</details>

<details open><summary><code>NOESCAPE</code></summary> 

is present for legacy compatibility and has no other effect.

</details>

:::note Note

 
Produce pretty-formatted JSON with `redis-cli` by following this example:

``` bash
~/$ redis-cli --raw
dragonfly> JSON.GET myjsonkey INDENT "\t" NEWLINE "\n" SPACE " " path.to.value[1]
```


:::

## Return

JSON.GET returns a bulk string representing a JSON array of string replies. 
Each string is the JSON serialization of each JSON value that matches a path. 
Using multiple paths, JSON.GET returns a bulk string representing a JSON object with string values. 
Each string value is an array of the JSON serialization of each JSON value that matches a path.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec).

## Examples

<details open>
<summary><b>Return the value at <code>path</code> in JSON serialized form</b></summary>

Create a JSON document.

``` bash
dragonfly> JSON.SET doc $ '{"a":2, "b": 3, "nested": {"a": 4, "b": null}}'
OK
```

With a single JSONPath (JSON array bulk string):

``` bash
dragonfly> JSON.GET doc $..b
"[3,null]"
```

Using multiple paths with at least one JSONPath returns a JSON string with a top-level object with an array of JSON values per path:

``` bash
dragonfly> JSON.GET doc ..a $..b
"{\"$..b\":[3,null],\"..a\":[2,4]}"
```

</details>

## See also

`JSON.SET` | `JSON.MGET` 
