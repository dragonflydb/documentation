---
description: Discover using Redis JSON.MSET command to write multiple JSON documents into a datastore.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.MSET

<PageTitle title="Redis JSON.MSET Command (Documentation) | Dragonfly" />

## Syntax

    JSON.MSET key path value [key path value ...]

**Time complexity:** O(K*(M+N)) where K is the aggregate of all matching paths for the provided keys,
M is the size of the original value, and N is the size of the new value.

**ACL categories:** @json

Atomically sets the JSON value in each node identified by applying the `path` argument to a JSON object for each `key`.
If `$` is used as the path, the entire object is overwritten or created with the provided value.

[Examples](#examples)

## Return

JSON.MSET returns "OK" in case of success, or error otherwise.

## Examples

```bash
dragonfly> JSON.MSET key1 $ '{"a":1}' key2 $ '{"b": 2}'
OK
dragonfly> JSON.GET key1 $
"[{\"a\":1}]"
dragonfly> JSON.MSET key1 $.c 2
OK
dragonfly> JSON.GET key1 $
"[{\"a\":1,\"c\":2}]"
```

## See also

`JSON.MSET` | `JSON.SET`
