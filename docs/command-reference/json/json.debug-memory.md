---
description: Learn how to use Redis `JSON.DEBUG MEMORY` to get the memory size in bytes of JSON values for efficient debugging and memory management.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.DEBUG MEMORY

<PageTitle title="Redis `JSON.DEBUG MEMORY` Command (Documentation) | Dragonfly" />

## Syntax

    JSON.DEBUG MEMORY key [path]

**Time complexity:** O(N) when path is evaluated to a single value, where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

Report the memory size in bytes of the JSON element.

[Examples](#examples)

## Required arguments

<details open><summary><code>key</code></summary>

is key to analyze.
</details>

## Optional arguments

<details open><summary><code>path</code></summary>

is JSONPath to specify. Default is root `$` if not provided.
</details>

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): memory size in bytes of the JSON value when path is evaluated to a single value.

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list that represents the memory size in bytes of JSON value at each path when path is evaluated to multiple values.

**Note:** Primitive JSON types (numbers, booleans, and `null`) return `0` because they are stored inline and do not allocate separate memory. Objects, arrays, and strings (that exceed the Small String Optimization buffer) return their actual heap-allocated memory size.

## Examples

<details open>
<summary><b>Check memory usage of different JSON types</b></summary>

Primitive types (numbers, booleans, null) return 0 bytes as they are stored inline:

```shell
dragonfly> JSON.SET primitives $ '{"num":42, "bool":true, "null":null}'
OK

dragonfly> JSON.DEBUG MEMORY primitives $.num
1) (integer) 0

dragonfly> JSON.DEBUG MEMORY primitives $.bool
1) (integer) 0

dragonfly> JSON.DEBUG MEMORY primitives $.null
1) (integer) 0
```

</details>

<details open>
<summary><b>Check memory usage of objects and arrays</b></summary>

Objects and arrays allocate memory and return their size in bytes:

```shell
dragonfly> JSON.SET obj_doc $ '{"a":1, "b":2, "c":{"k1":1,"k2":2}}'
OK

dragonfly> JSON.DEBUG MEMORY obj_doc $.c
1) (integer) 336

dragonfly> JSON.DEBUG MEMORY obj_doc $
1) (integer) 1104

dragonfly> JSON.SET arr_doc $ '[1, 2, 3, 4, 5]'
OK

dragonfly> JSON.DEBUG MEMORY arr_doc $
1) (integer) 80
```

</details>

<details open>
<summary><b>Check memory usage of strings</b></summary>

Short strings may be optimized (SSO - Small String Optimization) and return 0, while longer strings allocate memory:

```shell
dragonfly> JSON.SET short_str $ '{"text":"Hi"}'
OK

dragonfly> JSON.DEBUG MEMORY short_str $.text
1) (integer) 0

dragonfly> JSON.SET long_str $ '{"text":"This is a longer string that should definitely exceed SSO buffer"}'
OK

dragonfly> JSON.DEBUG MEMORY long_str $.text
1) (integer) 112
```

</details>

<details open>
<summary><b>Check memory usage of multiple paths</b></summary>

When using JSONPath expressions that match multiple values, returns an array of memory sizes:

```shell
dragonfly> JSON.SET doc $ '[1, 2.3, "foo", true, null, {}, [], {"a":1, "b":2}, [1,2,3]]'
OK

dragonfly> JSON.DEBUG MEMORY doc $[*]
1) (integer) 0   # 1
2) (integer) 0   # 2.3
3) (integer) 0   # "foo"
4) (integer) 0   # true
5) (integer) 0   # null
6) (integer) 0   # {}
7) (integer) 0   # []
8) (integer) 336  # {"a":1, "b":2}
9) (integer) 48  # [1,2,3]
```

</details>

## See also

[`JSON.DEBUG FIELDS`](./json.debug-fields.md) | [`JSON.DEBUG HELP`](./json.debug-help.md)

## Related Topics

- [RedisJSON](https://redis.io/docs/latest/develop/data-types/json/)
- [Index and search JSON documents](https://redis.io/docs/latest/develop/data-types/json/indexing_json/)

