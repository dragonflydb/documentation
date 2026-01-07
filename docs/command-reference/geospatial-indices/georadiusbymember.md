---
description: "Learn how to use GEORADIUSBYMEMBER to add geographical data to your Dragonfly database by defining latitude and longitude."
---

import PageTitle from '@site/src/components/PageTitle';

# GEORADIUSBYMEMBER

<PageTitle title="GEORADIUSBYMEMBER Command (Documentation) | Dragonfly" />

## Syntax

```
GEORADIUSBYMEMBER key member radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC] [STORE key | STOREDIST key]
```

**Time complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**ACL categories:** @write, @geo, @slow

This command is exactly like `GEORADIUS` with the sole difference that, it accepts the name of a member already existing inside the geospatial index.

The position of the specified member is used as the center of the query.

## Return

  - If no `WITH*` option is specified, an array reply of matched member names
  - If `WITHCOORD`, `WITHDIST`, or `WITHHASH` options are specified, the command returns an array reply of arrays, where each sub-array represents a single item:
    - The distance from the center as a floating point number, in the same unit specified in the radius.
    - The Geohash integer.
    - The coordinates as a two items x,y array (longitude,latitude).

## Examples

```shell
dragonfly> GEOADD Greece 11.994038 31.792256 "Thessaloniki"
(integer) 1
dragonfly> GEOADD Greece  37.983810 23.727539 "Athens" 39.62069 19.91975 "Corfu"
(integer) 2
dragonfly> GEORADIUSBYMEMBER Greece Thessaloniki 1000 km
1) "Corfu"
2) "Thessaloniki"
3) "Athens"
```
