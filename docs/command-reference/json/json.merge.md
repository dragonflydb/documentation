---
description: Discover using Redis JSON.MERGE command to merge one JSON document into another.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.MERGE

<PageTitle title="Redis JSON.MERGE Command (Documentation) | Dragonfly" />

## Syntax

    JSON.MERGE key path value

**Time complexity:** O(M+N) where M is the size of the original json object located at `key`,
and N is the size of the value merged into it.

**ACL categories:** @json

The `JSON.MERGE` command merges a provided JSON value into matching paths within
the existing JSON object at the specified `key`.
This operation can result in updates, deletions, or the creation of new children within the target object.

**Merge Behavior:**
* Matching paths in the original object are updated with the corresponding values from the provided JSON.
* Non-existent paths in the original object are created as new children with the values from the provided JSON.
* Existing paths can be deleted if the corresponding value in the provided JSON is `null`.

**Standard Compliance:**

This command adheres to the specifications outlined in [RFC7396](https://datatracker.ietf.org/doc/html/rfc7396).


## Return

JSON.MERGE returns "OK" in case of success, or error otherwise.

## Examples

Update the existing document:

```bash
dragonfly> JSON.SET key $ '{"a":1, "b" : 2}'
OK
dragonfly> JSON.MERGE key $ '{"b" : 3}'
OK
dragonfly> JSON.GET key $
"[{\"a\":1,\"b\":3}]"

dragonfly> JSON.MERGE key $.b 4
OK
dragonfly> JSON.GET key $
"[{\"a\":1,\"b\":4}]"
```

Create a new path or value:

```bash
dragonfly> JSON.MERGE new $ '{"b" : 3}'
OK
dragonfly> JSON.GET new $
"[{\"b\":3}]"

dragonfly> JSON.MERGE new $ '{"c" : "another"}'
dragonfly> JSON.GET new $
"[{\"b\":3,\"c\":\"another\"}]"
```

Delete paths:

```bash
dragonfly> JSON.SET key $ '{"one" : 1, "two": 2}'
OK
dragonfly> JSON.MERGE key $ '{"one" : null}'
OK
dragonfly> JSON.GET key $
"[{\"two\":2}]"
```
