---
description: Understand Redis JSON.NUMMULTBY command to multiply a numeric value within a JSON document.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.NUMMULTBY

<PageTitle title="Redis JSON.NUMMULTBY Command (Documentation) | Dragonfly" />

## Syntax

    JSON.NUMMULTBY key path value

**Time complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Multiply the number value stored at `path` by `number`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary> 

is key to modify.

</details>

<details open><summary><code>value</code></summary> 

is number value to multiply. 

</details>

## Optional arguments

<details open><summary><code>path</code></summary> 

is JSONPath to specify. Default is root `$`.

</details>

## Return

JSON.NUMMULTBY returns a bulk string reply specified as a stringified new values for each path, or `nil` element if the matching JSON value is not a number.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec).

## Examples

``` bash
dragonfly> JSON.SET doc . '{"a":"b","b":[{"a":2}, {"a":5}, {"a":"c"}]}'
OK
dragonfly> JSON.NUMMULTBY doc $.a 2
"[null]"
dragonfly> JSON.NUMMULTBY doc $..a 2
"[null,4,10,null]"
```

## See also

`JSON.NUMINCRBY` | `JSON.ARRINSERT` 
