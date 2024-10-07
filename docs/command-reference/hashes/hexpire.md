---
description: "HEXPIRE command to set the expiration time of specific values."
---

import PageTitle from '@site/src/components/PageTitle';

# HEXPIRE

<PageTitle title="Redis HEXPIRE Command (Documentation) | Dragonfly" />

## Syntax

    HEXPIRE key seconds FIELDS numfields field [field field ...]

**Time complexity:** O(N) where N is the number of arguments to the command

**ACL categories:** @write, @hash, @fast

Set an expiration (TTL or time to live) on one or more fields of a given hash key. You must specify at least one field. 
Field(s) will automatically be deleted from the hash key when their TTLs expire.


## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): 
* Integer reply: -2 if no such field exists in the provided hash key, or the provided key does not exist.
* Integer reply: 1 if the expiration time was set/updated.
* Integer reply: 2 when HEXPIRE is called with 0 seconds/milliseconds or when HEXPIREAT is called with a past Unix time in seconds/milliseconds.
[Simple reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-errors): The number of fields that were added.
* if parsing failed, mandatory arguments are missing, unknown arguments are specified, or argument values are of the wrong type or out of range.
* if the provided key exists but is not a hash.


## Examples

```shell
dragonfly> HEXPIRE no-key 20 FIELDS 2 field1 field2
(nil)
dragonfly> HSET mykey field1 "hello" field2 "world"
(integer 2)
dragonfly> HEXPIRE mykey 10 FIELDS 3 field1 field2 field3
1) (integer) 1
2) (integer) 1
3) (integer) -2
dragonfly> HGETALL mykey
(empty array)
```
