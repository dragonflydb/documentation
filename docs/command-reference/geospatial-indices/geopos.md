---
description: Get the positions of specified members in a geospatial index
---

# GEOPOS

## Syntax

    GEOPOS key [member [member ...]]

**Time complexity:** O(N) where N is the number of members requested.

Return the positions (longitude, latitude) of all the specified members of the geospatial index represented by the sorted set.

Given a sorted set representing a geospatial index, populated using the [`GEOADD`](./geoadd.md) command, it is often useful to obtain back the coordinates of specified members.
When the geospatial index is populated via [`GEOADD`](./geoadd.md) the coordinates are converted into a 52 bit Geohash,
so the coordinates returned may not be exactly the ones used in order to add the elements, but small errors may be introduced.

The command can accept a variable number of arguments, so it always returns an array of positions even when a single element is specified.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#resp-arrays), specifically:

The command returns an array where each element is a two elements array representing longitude and latitude (x,y) of each member name passed as argument to the command.

Non-existing elements are reported as NULL elements of the array.

## Examples

```shell
dragonfly> GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
(integer) 2
dragonfly> GEOPOS Sicily Palermo Catania NonExisting
1) 1) "13.36138933897018433"
   2) "38.11555639549629859"
2) 1) "15.08726745843887329"
   2) "37.50266842333162032"
3) (nil)
```
