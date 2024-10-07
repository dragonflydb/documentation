---
description: "FIELDEXPIRE command to set the expiration time of specific values for hset and set family."
---

import PageTitle from '@site/src/components/PageTitle';

# HEXPIRE

<PageTitle title="Dragonfly specific FIELDEXPIRE Command (Documentation) | Dragonfly" />

## Syntax

    FIELDEXPIRE key seconds field [field field ...]

**Time complexity:** O(N) where N is the number of arguments to the command

**ACL categories:** @write, @set, @hash, @fast

Set an expiration (TTL or time to live) on one or more fields of a given hash key. You must specify at least one field. 
Field(s) will automatically be deleted from the hash key when their TTLs expire.


## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): 
* Integer reply: -2 if no such field exists in the provided hash key, or the provided key does not exist.
* Integer reply: 1 if the expiration time was set/updated.
* Integer reply: 2 when FIELDEXPIRE is called with 0 seconds/milliseconds or when FIELDEXPIRE is called with a past Unix time in seconds/milliseconds.
[Simple reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-errors): The number of fields that were added.
* if parsing failed, mandatory arguments are missing, unknown arguments are specified, or argument values are of the wrong type or out of range.
* if the provided key exists but is not a hash.


## Examples

```shell
dragonfly> FIELDEXPIRE no-key 20 field1 field2
(nil)
dragonfly> HSET mykey field1 "hello" field2 "world"
(integer 2)
dragonfly> FIELDEXPIRE mykey 10 field1 field2 field3
1) (integer) 1
2) (integer) 1
3) (integer) -2
dragonfly> HGETALL mykey
(empty array)
```
