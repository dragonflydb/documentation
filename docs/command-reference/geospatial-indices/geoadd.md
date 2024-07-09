---
description: "Learn how to use Redis GEOADD to add geographical data to your Redis database by defining latitude and longitude."
---

import PageTitle from '@site/src/components/PageTitle';

# GEOADD

<PageTitle title="Redis GEOADD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

GEOADD is a command in Redis used to add geospatial items (latitude, longitude, and member) to a sorted set. This command is particularly useful for applications that require location-based services, such as finding nearby stores, tracking the locations of delivery vehicles, or any use case involving geolocation data.

## Syntax

```
GEOADD key longitude latitude member [longitude latitude member ...]
```

## Parameter Explanations

- **key**: The name of the sorted set to store the geospatial items.
- **longitude**: The longitude of the geospatial item. It must be a valid floating-point number.
- **latitude**: The latitude of the geospatial item. It must be a valid floating-point number.
- **member**: The name of the member to associate with the given coordinates.

You can add multiple geospatial items in one command by repeating the longitude, latitude, and member parameters.

## Return Values

The GEOADD command returns an integer representing the number of elements that were added to the sorted set (excluding any elements already existing for which the coordinates were updated).

Example:

```cli
dragonfly> GEOADD cities 13.361389 38.115556 \"Palermo\"
(integer) 1
dragonfly> GEOADD cities 15.087269 37.502669 \"Catania\"
(integer) 1
dragonfly> GEOADD cities 13.361389 38.115556 \"Palermo\"
(integer) 0
```

## Code Examples

```cli
dragonfly> GEOADD landmarks 2.294481 48.858370 \"Eiffel Tower\"
(integer) 1
dragonfly> GEOADD landmarks -0.126236 51.500729 \"Big Ben\"
(integer) 1
dragonfly> GEOADD landmarks 2.294481 48.858370 \"Eiffel Tower\"
(integer) 0
dragonfly> GEOPOS landmarks \"Eiffel Tower\"
1) 1) "2.294481"
   2) "48.858370"
dragonfly> GEODIST landmarks \"Eiffel Tower\" \"Big Ben\"
"343.3804"
```

## Best Practices

- When adding multiple members, try to do it in a single GEOADD command to reduce the number of network round trips and improve performance.
- Ensure that the longitude values are between -180 and 180 and latitude values are between -90 and 90 to avoid errors.

## Common Mistakes

- Using invalid longitude or latitude values will result in an error. Always validate your coordinates before using them in the GEOADD command.
- Forgetting that updating the coordinates of an existing member does not count as adding a new element (return value will be 0).

## FAQs

### What happens if I update the coordinates of an existing member?

If you update the coordinates of an existing member, the return value will be 0 because no new element was added; only the coordinates of an existing element were updated.

### Can I add multiple geospatial items in one command?

Yes, you can add multiple geospatial items in one GEOADD command by repeating the longitude, latitude, and member parameters.
