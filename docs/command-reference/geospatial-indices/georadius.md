---
description: "Learn how to use GEORADIUS to add geographical data to your Dragonfly database by defining latitude and longitude."
---

import PageTitle from '@site/src/components/PageTitle';

# GEORADIUS
 
<PageTitle title="GEORADIUS Command (Documentation) | Dragonfly" />

## Syntax

    GEORADIUS key longitude latitude radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC] [STORE key | STOREDIST key]

**Time complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**ACL categories:** @write, @geo, @slow

Return the members of a sorted set populated with geospatial information using GEOADD, which are within the borders of the area specified with the center location and the maximum distance from the center (the radius).

The radius is specified in one of the following units:
- `m` for meters.
- `km` for kilometers.
- `mi` for miles.
- `ft` for feet.

By default the command returns the items to the client. It is possible to store the results with one of these options:

- STORE: Store the items in a sorted set populated with their geospatial information.
- STOREDIST: Store the items in a sorted set populated with their distance from the center as a floating point number, in the same unit specified in the radius.

## Return

  - If no `WITH*` option is specified, an array reply of matched member names
  - If `WITHCOORD`, `WITHDIST`, or `WITHHASH` options are specified, the command returns an array reply of arrays, where each sub-array represents a single item:
    - The distance from the center as a floating point number, in the same unit specified in the radius.
    - The Geohash integer.
    - The coordinates as a two items x,y array (longitude,latitude).

The command default is to return unsorted items. Two different sorting methods can be invoked using the following two options:

- ASC: Sort returned items from the nearest to the farthest, relative to the center.
- DESC: Sort returned items from the farthest to the nearest, relative to the center.

By default all the matching items are returned. It is possible to limit the results to the first N matching items by using the COUNT option. When ANY is provided the command will return as soon as enough matches are found, so the results may not be the ones closest to the specified point, but on the other hand, the effort invested by the server is significantly lower. When ANY is not provided, the command will perform an effort that is proportional to the number of items matching the specified area and sort them, so to query very large areas with a very small COUNT option may be slow even if just a few results are returned.

## Examples

```shell
dragonfly> GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
(integer) 2
dragonfly> GEORADIUS Sicily 15 37 200 km WITHDIST
1) 1) "Palermo"
   2) "190.4424"
2) 1) "Catania"
   2) "56.4413"
dragonfly> GEORADIUS Sicily 15 37 200 km WITHCOORD
1) 1) "Palermo"
   2) 1) "13.36138933897018433"
      2) "38.11555639549629859"
2) 1) "Catania"
   2) 1) "15.08726745843887329"
      2) "37.50266842333162032"
dragonfly> GEORADIUS Sicily 15 37 200 km WITHDIST WITHCOORD
1) 1) "Palermo"
   2) "190.4424"
   3) 1) "13.36138933897018433"
      2) "38.11555639549629859"
2) 1) "Catania"
   2) "56.4413"
   3) 1) "15.08726745843887329"
      2) "37.50266842333162032"
```
