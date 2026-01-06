---
description: Learn how to use Redis JSON.ARRLEN command to find the length of a JSON array.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRLEN

<PageTitle title="Redis JSON.ARRLEN Command (Documentation) | Dragonfly" />

## Syntax

    JSON.ARRLEN key [path]

**Time complexity:** O(1) where path is evaluated to a single value, O(N) where path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Report the length of the JSON array at `path` in `key`

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary>

is key to parse.

</details>

## Optional arguments

<details open><summary><code>path</code></summary>

is JSONPath to specify. Default is root `$`, if not provided. Returns null if the `key` or `path` do not exist.

</details>

## Return

`JSON.ARRLEN` returns an [array](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays) of integer replies, an integer for each matching value, each is the array's length, or `nil`, if the matching value is not an array.
For more information about replies, see [Redis serialization protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec).

## Examples

<details open>
<summary><b>Get lengths of JSON arrays in a document</b></summary>

Create a document for wireless earbuds.

```bash
dragonfly> JSON.SET item:2 $ '{"name":"Wireless earbuds","description":"Wireless Bluetooth in-ear headphones","connection":{"wireless":true,"type":"Bluetooth"},"price":64.99,"stock":17,"colors":["black","white"], "max_level":[80, 100, 120]}'
OK
```

Find lengths of arrays in all objects of the document.

```bash
dragonfly> JSON.ARRLEN item:2 '$.*'
1) (nil)
2) (nil)
3) (nil)
4) (nil)
5) (nil)
6) (integer) 2
7) (integer) 3
```

Return the length of the `max_level` array.

```bash
dragonfly> JSON.ARRLEN item:2 '$..max_level'
1) (integer) 3
```

Get all the maximum level values.

```bash
dragonfly> JSON.GET item:2 '$..max_level'
"[[80,100,120]]"
```

</details>

## See also

`JSON.ARRINDEX` | `JSON.ARRINSERT`
