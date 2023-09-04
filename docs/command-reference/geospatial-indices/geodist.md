---
description: Get the distance between two members in a geospatial index
---

# GEODIST

## Syntax

    GEODIST key member1 member2 [M | KM | FT | MI]

**Time complexity:** O(log(N)), where N is the number of elements in the geospatial index represented by the sorted set.

**ACL categories:** @read, @geo, @slow

Return the distance between two members in the geospatial index represented by the sorted set.

Given a sorted set representing a geospatial index, populated using the [`GEOADD`](./geoadd.md) command, the command returns the distance between the two specified members in the specified unit.

If one or both the members are missing, the command returns NULL.

The unit must be one of the following, and defaults to meters:

- `m` for meters.
- `km` for kilometers.
- `mi` for miles.
- `ft` for feet.

The distance is computed assuming that the Earth is a perfect sphere, so errors up to 0.5% are possible in edge cases.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#resp-bulk-strings), specifically:

The command returns the distance as a double (represented as a string) in the specified unit, or NULL if one or both the elements are missing.

## Examples

```shell
dragonfly> GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
(integer) 2
dragonfly> GEODIST Sicily Palermo Catania
"166274.1516"
dragonfly> GEODIST Sicily Palermo Catania km
"166.2742"
dragonfly> GEODIST Sicily Palermo Catania mi
"103.3182"
dragonfly> GEODIST Sicily Foo Bar
(nil)
```
