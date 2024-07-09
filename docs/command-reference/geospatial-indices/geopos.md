---
description: "Learn how to use Redis GEOPOS to retrieve the longitude and latitude of a geographical point from your database."
---

import PageTitle from '@site/src/components/PageTitle';

# GEOPOS

<PageTitle title="Redis GEOPOS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GEOPOS` command in Redis is used to retrieve the positions (longitude, latitude) of specified members within a geospatial index represented by a sorted set. This can be particularly useful for applications involving location-based services, such as finding the coordinates of stores, landmarks, or users.

## Syntax

```plaintext
GEOPOS key member [member ...]
```

## Parameter Explanations

- `key`: The name of the sorted set representing the geospatial index.
- `member`: One or more members whose positions you want to retrieve. These members must be already added to the geospatial index.

## Return Values

The command returns an array of positions. Each position is represented as a two-element array where the first element is the longitude and the second is the latitude. If the member does not exist, the corresponding position will be `nil`.

### Example Outputs

1. If all members exist:
   ```plaintext
   1) 1) "13.361389338970184"
      2) "38.115556395496299"
   ```
2. If some members do not exist:
   ```plaintext
   1) 1) "13.361389338970184"
      2) "38.115556395496299"
   2) (nil)
   ```

## Code Examples

```cli
dragonfly> ZADD mygeo 13.361389 38.115556 "Palermo"
(integer) 1
dragonfly> ZADD mygeo 15.087269 37.502669 "Catania"
(integer) 1
dragonfly> GEOPOS mygeo "Palermo" "Catania"
1) 1) "13.361389338970184"
   2) "38.115556395496299"
2) 1) "15.087267458438873"
   2) "37.50266842333162"
dragonfly> GEOPOS mygeo "Nonexistent"
1) (nil)
```

## Best Practices

- Ensure that the members you query with `GEOPOS` have been added to the geospatial index using `GEOADD`.
- Regularly update the positions if they are subject to change to maintain accurate geolocation data.

## Common Mistakes

- Querying for members that do not exist in the geospatial index, which results in `nil` values.
- Misunderstanding the order of the returned coordinates; it is always in the order `[longitude, latitude]`.

## FAQs

### What happens if I request the position of a member not in the index?

If a member is not in the index, `GEOPOS` will return `nil` for that member.

### Can I use `GEOPOS` with non-geospatial data?

No, `GEOPOS` is specifically designed for retrieving geospatial (longitude, latitude) data from a sorted set created with `GEOADD`.
