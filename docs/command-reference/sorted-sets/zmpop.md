---
description: Learn to use the Redis ZMPOP command to remove and return the smallest score member from sorted sets.
---

import PageTitle from '@site/src/components/PageTitle';

# ZMPOP

<PageTitle title="Redis ZMPOP Explained" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZMPOP` command pops one or more members (element-score pairs) from the first non-empty sorted set in the provided list of key names.

## Syntax

```shell
ZMPOP numkeys key [key ...] <MIN | MAX> [COUNT count]
```

- **Time complexity:** O(K) + O(M*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.
- **ACL categories:** @write, @sortedset, @slow

When the `MIN` modifier is used, the elements popped are those with the lowest scores from the first non-empty sorted set.
The `MAX` modifier causes elements with the highest scores to be popped. 
The optional `COUNT` can be used to specify the number of elements to pop, and is set to 1 by default.

The number of popped elements is the minimum from the sorted set's cardinality and `COUNT`'s value.

See [`BZMPOP`](./bzmpop) for the blocking variant of this command.

## Return Values

- [Null reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#nulls): when no member could be popped.
- [Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a two-element array with the first element
  being the name of the key from which members were popped, and the second element is an array of the popped members.
  Every entry in the elements array is also an array that contains the member and its score.

## Code Examples

### Pop from a Single Sorted Set

```shell
dragonfly$> ZADD key 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4

dragonfly$> ZMPOP 1 key MIN
1) "key"
2) 1) 1) "one"
      2) "1"

dragonfly$> ZRANGE key 0 -1
1) "two"
2) "three"
3) "four"

dragonfly$> ZMPOP 1 key MAX COUNT 2
1) "key"
2) 1) 1) "four"
      2) "4"
   2) 1) "three"
      2) "3"

dragonfly$> ZRANGE key 0 -1
1) "two"
```

### Pop from Multiple Sorted Sets

```shell
dragonfly$> ZADD key1 1 "one" 2 "two"
(integer) 2
dragonfly$> ZADD key2 3 "three" 4 "four"
(integer) 2

dragonfly$> ZMPOP 2 key1 key2 MIN COUNT 2
1) "key1"
2) 1) 1) "one"
      2) "1"
   2) 1) "two"
      2) "2"

dragonfly$> ZRANGE key1 0 -1
(empty array)
dragonfly$> ZRANGE key2 0 -1
1) "three"
2) "four"

# Now the first key is empty. ZMPOP will pop elements from the next key.
dragonfly$> ZMPOP 2 key1 key2 MIN COUNT 2
1) "key2"
2) 1) 1) "three"
      2) "3"
   2) 1) "four"
      2) "4"

dragonfly$> ZRANGE key1 0 -1
(empty array)
dragonfly$> ZRANGE key2 0 -1
(empty array)
```

### No Element to Pop

```shell
dragonfly$> ZMPOP 1 non-existent MIN
(nil)
```
