---
description:  Learn how to use Redis LMPOP to remove and get elements from the first non-empty list.
---
import PageTitle from '@site/src/components/PageTitle';

# LMPOP

<PageTitle title="Redis LMPOP Command (Documentation) | Dragonfly" />

## Syntax

    LMPOP numkeys key [key ...] <LEFT | RIGHT> [COUNT count]

**Time complexity:** O(N+M) where N is the number of provided keys and M is the number of elements returned.

**ACL categories:** @write, @list, @slow

Pops one or more elements from the first non-empty list key from the list of provided key names.

Elements are popped from either the left or right of the first non-empty list based on the passed argument. The number of returned elements is limited to the lower between the non-empty list's length, and the count argument (which defaults to 1).

## Return

## Examples

```shell
dragonfly> LMPOP 2 non1 non2 LEFT COUNT 10
(nil)
dragonfly> LPUSH mylist "one" "two" "three" "four" "five"
(integer) 5
dragonfly> LMPOP 1 mylist LEFT
1) "mylist"
2) 1) "five"
dragonfly> LRANGE mylist 0 -1
1) "four"
2) "three"
3) "two"
4) "one"
dragonfly> LMPOP 1 mylist RIGHT COUNT 10
1) "mylist"
2) 1) "one"
   2) "two"
   3) "three"
   4) "four"
dragonfly> LPUSH mylist "one" "two" "three" "four" "five"
(integer) 5
dragonfly> LPUSH mylist2 "a" "b" "c" "d" "e"
(integer) 5
dragonfly> LMPOP 2 mylist mylist2 right count 3
1) "mylist"
2) 1) "one"
   2) "two"
   3) "three"
dragonfly> LRANGE mylist 0 -1
1) "five"
2) "four"
dragonfly> LMPOP 2 mylist mylist2 right count 5
1) "mylist"
2) 1) "four"
   2) "five"
dragonfly> LMPOP 2 mylist mylist2 right count 10
1) "mylist2"
2) 1) "a"
   2) "b"
   3) "c"
   4) "d"
   5) "e"
dragonfly> EXISTS mylist mylist2
(integer) 0
```