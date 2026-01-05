---
description: "Learn how to use Redis GEOSEARCHSTORE to search and store geospatial data in your Redis database."
---

import PageTitle from '@site/src/components/PageTitle';

# GEOSEARCHSTORE

<PageTitle title="Redis GEOSEARCHSTORE Command (Documentation) | Dragonfly" />

## Syntax

    GEOSEARCHSTORE destination source <FROMMEMBER member | FROMLONLAT longitude latitude>
    <BYRADIUS radius <M | KM | FT | MI> | BYBOX width height <M | KM | FT | MI>>
    [ASC | DESC] [COUNT count [ANY]] [STOREDIST]

**Time complexity:** O(N+log(M)) where N is the number of elements in the grid-aligned bounding box
area around the shape provided as the filter and M is the number of items inside the shape.

**ACL categories:** @write, @geo, @slow

This command is like [GEOSEARCH](./geosearch), but stores the result in destination key.

By default, it stores the results as member names. When the `STOREDIST` option is used, the command stores the items in a sorted set populated with their distance from the center of the circle or box, as a floating-point number, in the same unit specified for that shape.

## Query Center Point

The query's center point is provided by one of these mandatory options:

* `FROMMEMBER`: Use the position of the given existing `<member>` in the sorted set.
* `FROMLONLAT`: Use the given `<longitude>` and `<latitude>` position.

## Query Shape

The query's shape is provided by one of these mandatory options:

* `BYRADIUS`: Search inside circular area according to given `<radius>`.
* `BYBOX`: Search inside an axis-aligned rectangle, determined by `<height>` and `<width>`.

## Query Options

* `ASC`: Sort returned items from the nearest to the farthest, relative to the center point.
* `DESC`: Sort returned items from the farthest to the nearest, relative to the center point.
* `COUNT count [ANY]`: Limit the results to the first N matching items. When the `ANY` option is used, the command returns as soon as enough matches are found, which means the results may not be the ones closest to the specified point, but the effort invested by the server is significantly lower.
* `STOREDIST`: Store the distance of the returned items from the center point as the sorted set score, instead of the geospatial information.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): the number of elements in the resulting set.

## Examples

```shell
dragonfly> GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
(integer) 2

dragonfly> GEOADD Sicily 12.758489 38.788135 "edge1" 17.241510 38.788135 "edge2"
(integer) 2

dragonfly> GEOSEARCHSTORE result Sicily FROMLONLAT 15 37 BYBOX 400 400 KM ASC COUNT 3
(integer) 3

dragonfly> ZRANGE result 0 -1
1) "Catania"
2) "Palermo"
3) "edge2"

dragonfly> GEOSEARCHSTORE result_with_dist Sicily FROMLONLAT 15 37 BYBOX 400 400 KM ASC COUNT 3 STOREDIST
(integer) 3

dragonfly> ZRANGE result_with_dist 0 -1 WITHSCORES
1) "Catania"
2) "56.4412578701582"
3) "Palermo"
4) "190.44242984775784"
5) "edge2"
6) "279.7403417843143"

dragonfly> GEOSEARCHSTORE result_radius Sicily FROMMEMBER Palermo BYRADIUS 100 KM
(integer) 1

dragonfly> ZRANGE result_radius 0 -1
1) "Palermo"
```
