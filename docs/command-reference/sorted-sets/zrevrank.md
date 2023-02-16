---
description: Determine the index of a member in a sorted set, with scores
  ordered from high to low
---

# ZREVRANK

## Syntax

    ZREVRANK key member [WITHSCORE]

**Time complexity:** O(log(N))

Returns the rank of `member` in the sorted set stored at `key`, with the scores
ordered from high to low.
The rank (or index) is 0-based, which means that the member with the highest
score has rank `0`.

The optional `WITHSCORE` argument supplements the command's reply with the score of the element returned.

Use `ZRANK` to get the rank of an element with the scores ordered from low to
high.

## Return

* If `member` exists in the sorted set:
  * using `WITHSCORE`, [Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): an array containing the rank and score of `member`.
  * without using `WITHSCORE`, [Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the rank of `member`.
* If `member` does not exist in the sorted set or `key` does not exist:
  * using `WITHSCORE`, [Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): `nil`.
  * without using `WITHSCORE`, [Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): `nil`.
  
Note that in RESP3 null and nullarray are the same, but in RESP2 they are not.

## Examples

```cli
ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZADD myzset 3 "three"
ZREVRANK myzset "one"
ZREVRANK myzset "four"
ZREVRANK myzset "three" WITHSCORE
ZREVRANK myzset "four" WITHSCORE
```
