---
acl_categories:
- '@read'
- '@string'
- '@fast'
arguments:
- key_spec_index: 0
  name: key
  type: key
arity: 2
command_flags:
- readonly
- fast
complexity: O(1)
description: Get the value of a key
github_branch: main
github_path: /tmp/docs/content/commands/get/index.md
github_repo: https://dragonflydb/redis-doc
group: string
hidden: false
key_specs:
- RO: true
  access: true
  begin_search:
    spec:
      index: 1
    type: index
  find_keys:
    spec:
      keystep: 1
      lastkey: 0
      limit: 0
    type: range
linkTitle: GET
since: 1.0.0
summary: Get the value of a key
syntax_fmt: GET key
syntax_str: ''
title: GET
---
Get the value of `key`.
If the key does not exist the special value `nil` is returned.
An error is returned if the value stored at `key` is not a string, because `GET`
only handles string values.

## Return

[Bulk string reply](/docs/reference/protocol-spec#resp-bulk-strings): the value of `key`, or `nil` when `key` does not exist.

## Examples

```cli
GET nonexisting
SET mykey "Hello"
GET mykey
```
