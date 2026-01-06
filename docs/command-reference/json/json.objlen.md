---
description: Learn using Redis JSON.OBJLEN command to get the length of a JSON object.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.OBJLEN

<PageTitle title="Redis JSON.OBJLEN Command (Documentation) | Dragonfly" />

## Syntax

    JSON.OBJLEN key [path]

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Report the number of keys in the JSON object at `path` in `key`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to parse. Returns `null` for nonexistent keys.

</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`. Returns `null` for nonexistant path.

</details>

## Return

JSON.OBJLEN returns an array of integer replies for each path specified as the number of keys in the object or `nil`, if the matching JSON value is not an object.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec).

## Examples

``` bash
dragonfly> JSON.SET doc $ '{"a":[3], "nested": {"a": {"b":2, "c": 1}}}'
OK
dragonfly> JSON.OBJLEN doc $..a
1) (nil)
2) (integer) 2
```

## See also

`JSON.ARRINDEX` | `JSON.ARRINSERT` 
