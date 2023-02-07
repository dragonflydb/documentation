---
acl_categories:
- '@read'
- '@list'
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
description: Get the length of a list
github_branch: main
github_path: /tmp/docs/content/commands/llen/index.md
github_repo: https://dragonflydb/redis-doc
group: list
hidden: false
key_specs:
- RO: true
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
linkTitle: LLEN
since: 1.0.0
summary: Get the length of a list
syntax_fmt: LLEN key
syntax_str: ''
title: LLEN
---
Returns the length of the list stored at `key`.
If `key` does not exist, it is interpreted as an empty list and `0` is returned.
An error is returned when the value stored at `key` is not a list.

## Return

[Integer reply](/docs/reference/protocol-spec#resp-integers): the length of the list at `key`.

## Examples

```cli
LPUSH mylist "World"
LPUSH mylist "Hello"
LLEN mylist
```
