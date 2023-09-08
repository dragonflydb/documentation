---
description: Shows helpful information
---

# JSON.DEBUG HELP

## Syntax

    JSON.DEBUG HELP 

**Time complexity:** N/A

**ACL categories:** @json

Return helpful information about the [`JSON.DEBUG`](./json.debug.md) command.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): a list of helpful messages.

## Examples

```shell
dragonfly> JSON.DEBUG HELP
1) "JSON.DEBUG FIELDS <key> <path> - report number of fields in the JSON element."
2) "JSON.DEBUG HELP - print help message."
```

## Related Topics

* [RedisJSON](https://redis.io/docs/stack/json)
* [Index and search JSON documents](https://redis.io/docs/stack/search/indexing_json)
