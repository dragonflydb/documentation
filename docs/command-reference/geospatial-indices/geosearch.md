---
description: "Learn how to use Redis GEOSEARCH to search your geospatial data in your Redis database."
---

import PageTitle from '@site/src/components/PageTitle';

# GEOSEARCH

<PageTitle title="Redis GEOSEARCH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GEOSEARCH` command in Redis is used to query a sorted set representing a geospatial index. It allows users to search for members within a given radius or rectangular area from a central point. Typical scenarios include finding nearby stores, services, or points of interest based on user location.

## Syntax

```plaintext
GEOSEARCH key FROMMEMBER member BYRADIUS radius unit [WITHCOORD] [WITHDIST] [COUNT count] [ASC|DESC]
GEOSEARCH key FROMLOC lon lat BYRADIUS radius unit [WITHCOORD] [WITHDIST] [COUNT count] [ASC|DESC]
GEOSEARCH key FROMMEMBER member BYBOX width height unit [WITHCOORD] [WITHDIST] [COUNT count] [ASC|DESC]
GEOSEARCH key FROMLOC lon lat BYBOX width height unit [WITHCOORD] [WITHDIST] [COUNT count] [ASC|DESC]
```

## Parameter Explanations

- `key`: The name of the sorted set containing the geospatial data.
- `FROMMEMBER member`: Specifies the reference member whose location will be used as the center for the search.
- `FROMLOC lon lat`: Specifies longitude and latitude directly as the center for the search.
- `BYRADIUS radius unit`: Searches within a circular area defined by the radius and unit (`m`, `km`, `ft`, `mi`).
- `BYBOX width height unit`: Searches within a rectangular area defined by width, height, and unit.
- `WITHCOORD`: Optional flag to include coordinates in the returned results.
- `WITHDIST`: Optional flag to include distance from the center in the returned results.
- `COUNT count`: Limits the number of results returned.
- `ASC|DESC`: Sorts the results in ascending or descending order based on distance.

## Return Values

The `GEOSEARCH` command returns an array of matching members. If `WITHCOORD` or `WITHDIST` options are specified, it includes additional arrays with coordinates and/or distances:

- Without flags: `[member1, member2, ...]`
- With `WITHDIST`: `[[member1, distance1], [member2, distance2], ...]`
- With `WITHCOORD`: `[[member1, [lon1, lat1]], [member2, [lon2, lat2]], ...]`
- With both `WITHDIST` and `WITHCOORD`: `[[member1, distance1, [lon1, lat1]], [member2, distance2, [lon2, lat2]], ...]`

## Code Examples

```cli
dragonfly> ZADD places 1 "place1" 2 "place2"
(integer) 2
dragonfly> GEOADD places 13.361389 38.115556 "Sicily"
(integer) 1
dragonfly> GEOADD places 15.087269 37.502669 "Catania"
(integer) 1
dragonfly> GEOSEARCH places FROMMEMBER Sicily BYRADIUS 200 km
1) "Sicily"
2) "Catania"
dragonfly> GEOSEARCH places FROMMEMBER Sicily BYRADIUS 200 km WITHDIST
1) 1) "Sicily"
   2) "0.0000"
2) 1) "Catania"
   2) "166.2742"
dragonfly> GEOSEARCH places FROMLOC 15 37 BYBOX 300 300 km ASC COUNT 1
1) "Catania"
```

## Best Practices

- Regularly update the geospatial data to maintain accuracy.
- Use the `COUNT` parameter to limit the number of results, improving performance for large datasets.
- Utilize `WITHDIST` and `WITHCOORD` to get more informative results.

## Common Mistakes

- Not specifying the correct unit (e.g., confusing meters with kilometers), which can lead to incorrect search results.
- Forgetting to use `ASC` or `DESC` to sort results, leading to unordered outputs, especially when limiting the results with `COUNT`.

## FAQs

### What units can be used with GEOSEARCH?

The accepted units are `m` (meters), `km` (kilometers), `ft` (feet), and `mi` (miles).

### How do I ensure my results include distances and coordinates?

Use the `WITHDIST` and `WITHCOORD` options to include distances and coordinates in the results.
