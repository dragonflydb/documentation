---
description: "Learn how to use Redis GEOHASH to convert latitude and longitude into a single string representing the geographical location."
---

import PageTitle from '@site/src/components/PageTitle';

# GEOHASH

<PageTitle title="Redis GEOHASH Command (Documentation) | Dragonfly" />

## Syntax

    GEOHASH key [member [member ...]]

**Time complexity:** O(log(N)) for each member requested, where N is the number of elements in the geospatial index represented by the sorted set.

**ACL categories:** @read, @geo, @slow

Return valid [Geohash](https://en.wikipedia.org/wiki/Geohash) strings representing the position of one or more elements
in a sorted set value representing a geospatial index (where elements were added using [`GEOADD`](./geoadd.md)).

## Geohash string properties

The command returns 11 characters Geohash strings, so no precision is lost compared to the Dragonfly internal 52 bit representation.
The returned Geohashes have the following properties:

- They can be shortened removing characters from the right. It will lose precision but will still point to the same area.
- It is possible to use them in `geohash.org` URLs such as `http://geohash.org/<geohash-string>`.
- Strings with a similar prefix are nearby, but the contrary is not true, it is possible that strings with different prefixes are nearby too.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays), specifically:

The command returns an array where each element is the Geohash corresponding to each member name passed as argument to the command.

## Examples

```shell
dragonfly> GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
(integer) 2
dragonfly> GEOHASH Sicily Palermo Catania
1) "sqc8b49rny0"
2) "sqdtr74hyu0"
```
