---
description: Report the number of fields in the JSON element
---

# JSON.DEBUG FIELDS

## Syntax

    JSON.DEBUG fields key path

**Time complexity:** N/A

**ACL categories:** @json

Report the number of fields in the JSON element.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): a list that represents the number of fields of JSON value at each path.

## Examples

Check number of fields in a JSON object.
Note that the command reports the total number of fields including those from child objects.

```shell
dragonfly> JSON.SET obj_doc $ '{"a":1, "b":2, "c":{"k1":1,"k2":2}}'
OK

dragonfly> JSON.DEBUG fields obj_doc '$.a'
1) (integer) 1

dragonfly> JSON.DEBUG fields obj_doc '$.b'
1) (integer) 1

dragonfly> JSON.DEBUG fields obj_doc '$.c'
1) (integer) 2

dragonfly> JSON.DEBUG fields obj_doc '$'
1) (integer) 5
```

Check number of fields in a JSON array.
Note that we can use JSONPath syntax including wildcards.

```shell
dragonfly> JSON.SET arr_doc . '[1, 2.3, "foo", true, null, {}, [], {"a":1,"b":2}, [1,2,3]]'
OK
 
dragonfly> JSON.GET arr_doc '$[*]'
"[1,2.3,\"foo\",true,null,{},[],{\"a\":1,\"b\":2},[1,2,3]]"
 
dragonfly> JSON.DEBUG fields arr_doc '$[*]'
1) (integer) 1  # 1
2) (integer) 1  # 2.3
3) (integer) 1  # "foo"
4) (integer) 1  # true
5) (integer) 1  # null
6) (integer) 0  # {}
7) (integer) 0  # []
8) (integer) 2  # {"a":1,"b":2}
9) (integer) 3  # [1,2,3]

dragonfly> JSON.DEBUG fields arr_doc '$[7,8]'
1) (integer) 2  # {"a":1,"b":2}
2) (integer) 3  # [1,2,3]
```
