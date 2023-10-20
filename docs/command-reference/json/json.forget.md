---
description: Know how to use Redis JSON.FORGET command for deleting a key-value pair from a JSON object.
---
import PageTitle from '@site/src/components/PageTitle';

# JSON.FORGET

<PageTitle title="Redis JSON.FORGET Command (Documentation) | Dragonfly" />

## Syntax

    JSON.FORGET key [path]

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the deleted value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

See `JSON.DEL`.
