---
description: Discover using Redis JSON.MGET command to retrieve multiple JSON documents from a database.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.MGET

<PageTitle title="Redis JSON.MGET Command (Documentation) | Dragonfly" />

## Syntax

    JSON.MGET key [key ...] path

**Time complexity:** O(M*N) when path is evaluated to a single value where M is the number of keys and N is the size of the value, O(N1+N2+...+Nm) when path is evaluated to multiple values where m is the number of keys and Ni is the size of the i-th key

**ACL categories:** @json

Return the values at `path` from multiple `key` arguments

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse. Returns `null` for nonexistent keys.

</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. Returns `null` for nonexistent paths.

</details>

## Return

JSON.MGET returns an array of bulk string replies specified as the JSON serialization of the value at each key's path.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec).

## Examples

<details open>
<summary><b>Return the values at <code>path</code> from multiple <code>key</code> arguments</b></summary> 

Create two JSON documents.

``` bash
dragonfly> JSON.SET doc1 $ '{"a":1, "b": 2, "nested": {"a": 3}, "c": null}'
OK
dragonfly> JSON.SET doc2 $ '{"a":4, "b": 5, "nested": {"a": 6}, "c": null}'
OK
```

Get values from all arguments in the documents.

``` bash
dragonfly> JSON.MGET doc1 doc2 $..a
1) "[1,3]"
2) "[4,6]"
```

</details>

## See also

`JSON.SET` | `JSON.GET` 
