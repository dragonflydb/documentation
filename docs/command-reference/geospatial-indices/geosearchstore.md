---
description: "Learn how to use GEOSEARCHSTORE to search your geospatial data and store the results in a new sorted set."
---

import PageTitle from '@site/src/components/PageTitle';

# GEOSEARCHSTORE

<PageTitle title="GEOSEARCHSTORE Command (Documentation) | Dragonfly" />

## Syntax

```
GEOSEARCHSTORE destination source <FROMMEMBER member |
 FROMLONLAT longitude latitude> <BYRADIUS radius <M | KM | FT | MI> |
 BYBOX width height <M | KM | FT | MI>> [ASC | DESC] [COUNT count [ANY]]
 [STOREDIST]
```

**Time complexity:** O(N+log(M)) where N is the number of elements in the grid-aligned bounding box
area around the shape provided as the filter and M is the number of items inside the shape.

**ACL categories:** @write, @geo, @slow

This command is like [`GEOSEARCH`](./geosearch.md), but stores the result in the `destination` key instead of returning it.
`source` must be a sorted set populated using [`GEOADD`](./geoadd.md).
If `destination` already exists, it is overwritten.

By default, the matching members are stored in `destination` with their geospatial information, so `destination` can be queried with other geospatial commands.
With the `STOREDIST` option, each member is stored with its distance from the center point as its score, as a floating point number, in the same unit as the radius or the width and height.

The query's center point is provided by one of these mandatory options:

* `FROMMEMBER`: Use the position of the given existing `<member>` in `source`. If the member does not exist, an error is returned.
* `FROMLONLAT`: Use the given `<longitude>` and `<latitude>` position.

The query's shape is provided by one of these mandatory options:

* `BYRADIUS`: Search inside a circular area according to the given `<radius>`.
* `BYBOX`: Search inside an axis-aligned rectangle, determined by `<width>` and `<height>`.

All matching items are stored by default. To store only N items, use the **COUNT `<count>`** option:

* Without `ANY`, all matching items are sorted, nearest first (or farthest first with `DESC`), and the first N are stored. So `COUNT <count>` stores the N nearest items and `COUNT <count> DESC` stores the N farthest items.
* With `ANY`, the first N matches found are kept and only then sorted, so they are not necessarily the nearest or the farthest items. This is cheaper than sorting all matches, but the server still scans every candidate in the search area.

`destination` is a sorted set, so its members are always ordered by their scores, whatever sorting option is used.

The `WITHCOORD`, `WITHDIST`, and `WITHHASH` options of `GEOSEARCH` are not accepted.

If no member matches, or `source` does not exist, `destination` is deleted and `0` is returned.

With key-based ACL rules, the user needs read access to `source` and write access to `destination`.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the number of elements in the resulting set.

## Examples

```shell
dragonfly> GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
(integer) 2
dragonfly> GEOADD Sicily 12.758489 38.788135 "edge1" 17.241510 38.788135 "edge2"
(integer) 2
dragonfly> GEOSEARCHSTORE key1 Sicily FROMLONLAT 15 37 BYBOX 400 400 km ASC COUNT 3
(integer) 3
dragonfly> GEOSEARCH key1 FROMLONLAT 15 37 BYBOX 400 400 km ASC WITHCOORD WITHDIST WITHHASH
1) 1) "Catania"
   2) "56.44125787015819"
   3) "3479447370796909"
   4) 1) "15.087267458438873"
      2) "37.50266842333162"
2) 1) "Palermo"
   2) "190.44242984775792"
   3) "3479099956230698"
   4) 1) "13.361389338970184"
      2) "38.1155563954963"
3) 1) "edge2"
   2) "279.7403417843142"
   3) "3481342659049484"
   4) 1) "17.241510450839996"
      2) "38.78813451624225"
dragonfly> GEOSEARCHSTORE key2 Sicily FROMLONLAT 15 37 BYBOX 400 400 km ASC COUNT 3 STOREDIST
(integer) 3
dragonfly> ZRANGE key2 0 -1 WITHSCORES
1) "Catania"
2) "56.44125787015819"
3) "Palermo"
4) "190.44242984775792"
5) "edge2"
6) "279.7403417843142"
```
