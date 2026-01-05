---
description: "Discover how to use Redis SORT command for sorting elements in list, set or sorted sets."
---

import PageTitle from '@site/src/components/PageTitle';

# SORT

<PageTitle title="Redis SORT Command (Documentation) | Dragonfly" />

## Syntax

    SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC | DESC] [ALPHA] [STORE destination]

**Time complexity:** O(N+M\*log(M)) where N is the number of elements in the list or set to sort, and M the number of returned elements. When the elements are not sorted, complexity is O(N).

**ACL categories:** @write, @set, @sortedset, @list, @slow, @dangerous

Returns or stores the elements contained in the [list][tdtl], [set][tdts] or
[sorted set][tdtss] at `key`.

By default, sorting is numeric and elements are compared by their value
interpreted as double precision floating point number.
This is `SORT` in its simplest form:

[tdtl]: https://redis.io/topics/data-types#lists
[tdts]: https://redis.io/topics/data-types#set
[tdtss]: https://redis.io/topics/data-types#sorted-sets

```
SORT mylist
```

Assuming `mylist` is a list of numbers, this command will return the same list
with the elements sorted from small to large.
In order to sort the numbers from large to small, use the `!DESC` modifier:

```
SORT mylist DESC
```

When `mylist` contains string values and you want to sort them
lexicographically, use the `!ALPHA` modifier:

```
SORT mylist ALPHA
```

Dragonfly is UTF-8 aware.

## Sorting by External Keys

The `BY` option allows sorting by external keys instead of the values in the collection itself:

```
SORT mylist BY weight_*
```

The `*` in the pattern is replaced with the values from the list.

## Retrieving External Keys

The `GET` option allows retrieving external keys instead of the elements themselves:

```
SORT mylist GET object_*
```

Multiple `GET` patterns can be specified to retrieve multiple values:

```
SORT mylist GET object_*->name GET object_*->email
```

## Storing Results

The `STORE` option stores the sorted result at the specified destination key instead of returning it:

```
SORT mylist STORE sorted_mylist
```

When using `STORE`, the command returns the number of elements stored.

The number of returned elements can be limited using the `!LIMIT` modifier.
This modifier takes the `offset` argument, specifying the number of elements to
skip and the `count` argument, specifying the number of elements to return from
starting at `offset`.
The following example will return 10 elements of the sorted version of `mylist`,
starting at element 0 (`offset` is zero-based):

```
SORT mylist LIMIT 0 10
```

Almost all modifiers can be used together.
The following example will return the first 5 elements, lexicographically sorted
in descending order:

```
SORT mylist LIMIT 0 5 ALPHA DESC
```

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): list of sorted elements.
