---
description: Add one or more members to a geospatial index
---

# GEOADD

## Syntax

    GEOADD key [NX | XX] [CH] longitude latitude member [longitude latitude member ...]

**Time complexity:** O(log(N)) for each item added, where N is the number of elements in the geospatial index represented by the sorted set.

**ACL categories:** @write, @geo, @slow

Adds the specified geospatial items (longitude, latitude, name) to the specified key.
Data is stored into the key as a sorted set, in a way that makes it possible to query the items with the `GEOSEARCH` command.

The command takes arguments in the standard format x,y so the longitude must be specified before the latitude.
There are limits to the coordinates that can be indexed: areas very near to the poles are not index-able.

## GEOADD options

`GEOADD` also provides the following options:

- `XX` -- Only update elements that already exist. Never add elements.
- `NX` -- Don't update already existing elements. Always add new elements.
- `CH` -- Modify the return value from the number of new elements added, to the total number of elements changed (`CH` is an abbreviation of changed).
Changed elements are new elements added and elements already existing for which the coordinates were updated.
So elements specified in the command line having the same score as they had in the past are not counted.
Normally, the return value of `GEOADD` only counts the number of new elements added.

Note: The `XX` and `NX` options are mutually exclusive.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#resp-integers), specifically:

- When used without optional arguments, the number of elements added to the sorted set (excluding score updates).
- If the `CH` option is specified, the number of elements that were changed (added or updated).

## Examples

```shell
dragonfly> GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
(integer) 2
dragonfly> GEODIST Sicily Palermo Catania
"166274.1516"
```
