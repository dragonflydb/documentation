---
acl_categories:
- '@write'
- '@list'
- '@slow'
arguments:
- name: numkeys
  type: integer
- key_spec_index: 0
  multiple: true
  name: key
  type: key
- arguments:
  - name: left
    token: LEFT
    type: pure-token
  - name: right
    token: RIGHT
    type: pure-token
  name: where
  type: oneof
- name: count
  optional: true
  token: COUNT
  type: integer
arity: -4
command_flags:
- write
- movablekeys
complexity: O(N+M) where N is the number of provided keys and M is the number of elements
  returned.
description: Pop elements from a list
github_branch: main
github_path: /tmp/docs/content/commands/lmpop/index.md
github_repo: https://dragonflydb/redis-doc
group: list
hidden: false
key_specs:
- RW: true
  access: true
  begin_search:
    spec:
      index: 1
    type: index
  delete: true
  find_keys:
    spec:
      firstkey: 1
      keynumidx: 0
      keystep: 1
    type: keynum
linkTitle: LMPOP
since: 7.0.0
summary: Pop elements from a list
syntax_fmt: "LMPOP numkeys key [key ...] <LEFT | RIGHT> [COUNT\_count]"
syntax_str: "key [key ...] <LEFT | RIGHT> [COUNT\_count]"
title: LMPOP
---
Pops one or more elements from the first non-empty list key from the list of provided key names.

`LMPOP` and [`BLMPOP`](/commands/blmpop) are similar to the following, more limited, commands:

- [`LPOP`](/commands/lpop) or [`RPOP`](/commands/rpop) which take only one key, and can return multiple elements.
- [`BLPOP`](/commands/blpop) or [`BRPOP`](/commands/brpop) which take multiple keys, but return only one element from just one key.

See [`BLMPOP`](/commands/blmpop) for the blocking variant of this command.

Elements are popped from either the left or right of the first non-empty list based on the passed argument.
The number of returned elements is limited to the lower between the non-empty list's length, and the count argument (which defaults to 1).

## Return

[Array reply](/docs/reference/protocol-spec#resp-arrays): specifically:

* A `nil` when no element could be popped.
* A two-element array with the first element being the name of the key from which elements were popped, and the second element is an array of elements.

## Examples

```cli
LMPOP 2 non1 non2 LEFT COUNT 10
LPUSH mylist "one" "two" "three" "four" "five"
LMPOP 1 mylist LEFT
LRANGE mylist 0 -1
LMPOP 1 mylist RIGHT COUNT 10
LPUSH mylist "one" "two" "three" "four" "five"
LPUSH mylist2 "a" "b" "c" "d" "e"
LMPOP 2 mylist mylist2 right count 3
LRANGE mylist 0 -1
LMPOP 2 mylist mylist2 right count 5
LMPOP 2 mylist mylist2 right count 10
EXISTS mylist mylist2
```
