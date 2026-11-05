---
description: Learn how to use Redis `JSON.DEBUG HELP` to understand how to troubleshoot JSON objects with this command.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.DEBUG HELP

<PageTitle title="Redis `JSON.DEBUG HELP` Command (Documentation) | Dragonfly" />

## Syntax

    JSON.DEBUG HELP

**Time complexity:** N/A

**ACL categories:** @json, @fast, @read

Return helpful information about the [`JSON.DEBUG`](./json.debug.md) command.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a list of helpful messages.

## Examples

```shell
dragonfly> JSON.DEBUG HELP
1) "JSON.DEBUG MEMORY <key> [path] - report memory size (bytes) of the JSON element. Path defaults to root if not provided."
2) "JSON.DEBUG FIELDS <key> [path] - report number of fields in the JSON element. Path defaults to root if not provided."
3) "JSON.DEBUG HELP - print help message."
```

## Related Topics

- [Valkey JSON](https://valkey.io/topics/valkey-json/)
- [Index JSON documents with Valkey Search](https://valkey.io/topics/search-data-formats/)
