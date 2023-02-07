---
acl_categories:
- '@write'
- '@hash'
- '@fast'
arguments:
- key_spec_index: 0
  name: key
  type: key
- arguments:
  - name: field
    type: string
  - name: value
    type: string
  multiple: true
  name: field_value
  type: block
arity: -4
command_flags:
- write
- denyoom
- fast
complexity: O(1) for each field/value pair added, so O(N) to add N field/value pairs
  when the command is called with multiple field/value pairs.
description: Set the string value of a hash field
github_branch: main
github_path: /tmp/docs/content/commands/hset/index.md
github_repo: https://dragonflydb/redis-doc
group: hash
hidden: false
history:
- - 4.0.0
  - Accepts multiple `field` and `value` arguments.
key_specs:
- RW: true
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
  update: true
linkTitle: HSET
since: 2.0.0
summary: Set the string value of a hash field
syntax_fmt: HSET key field value [field value ...]
syntax_str: field value [field value ...]
title: HSET
---
Sets `field` in the hash stored at `key` to `value`.
If `key` does not exist, a new key holding a hash is created.
If `field` already exists in the hash, it is overwritten.

## Return

[Integer reply](/docs/reference/protocol-spec#resp-integers): The number of fields that were added.

## Examples

```cli
HSET myhash field1 "Hello"
HGET myhash field1
```
