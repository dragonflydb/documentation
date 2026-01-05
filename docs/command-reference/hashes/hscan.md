---
description: "Learn how to use Redis HSCAN command to iteratively scan over a hash. Improve your data access strategy with this command."
---

import PageTitle from '@site/src/components/PageTitle';

# HSCAN

<PageTitle title="Redis HSCAN Command (Documentation) | Dragonfly" />

## Syntax

    HSCAN key cursor [MATCH pattern] [COUNT count] [NOVALUES]

**Time complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**ACL categories:** @read, @hash, @slow

See [SCAN](../generic/scan) for `HSCAN` documentation.

## Additional Option

* `NOVALUES`: When provided, the command returns only the field names without their values. This is useful when you need to enumerate hash keys without fetching their associated values, reducing memory usage and bandwidth.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays):

* Without `NOVALUES`: Returns an array where the first element is the cursor and the second element is an array of field-value pairs.
* With `NOVALUES`: Returns an array where the first element is the cursor and the second element is an array containing only field names.

## Examples

```shell
dragonfly> HSET myhash field1 "value1" field2 "value2" field3 "value3"
(integer) 3

dragonfly> HSCAN myhash 0
1) "0"
2) 1) "field1"
   2) "value1"
   3) "field2"
   4) "value2"
   5) "field3"
   6) "value3"

dragonfly> HSCAN myhash 0 NOVALUES
1) "0"
2) 1) "field1"
   2) "field2"
   3) "field3"
```
