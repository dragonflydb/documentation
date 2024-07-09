---
description: "Learn how to use Redis GEODIST to accurately calculate distances between geographical points in your data-set."
---

import PageTitle from '@site/src/components/PageTitle';

# GEODIST

<PageTitle title="Redis GEODIST Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GEODIST` command in Redis is used to calculate the distance between two geospatial points stored within a geospatial index (created using `GEOADD`). This command is useful for applications that need to measure the distance between locations, such as finding the distance between two cities or determining the proximity of users.

## Syntax

```cli
GEODIST key member1 member2 [unit]
```

## Parameter Explanations

- **key**: The name of the geospatial index.
- **member1**: The first member whose coordinates are to be used.
- **member2**: The second member whose coordinates are to be used.
- **unit**: Optional. The unit for the distance measurement. Possible values:
  - `m` for meters (default)
  - `km` for kilometers
  - `mi` for miles
  - `ft` for feet

## Return Values

The command returns the distance between the two specified members as a string representing a floating-point number. If any of the members do not exist in the set, it returns `nil`.

Examples of possible outputs:

- `"8287.062"` (distance in meters)
- `nil` (if one or both members do not exist)

## Code Examples

```cli
dragonfly> GEOADD mylocations 13.361389 38.115556 "Palermo"
(integer) 1
dragonfly> GEOADD mylocations 15.087269 37.502669 "Catania"
(integer) 1
dragonfly> GEODIST mylocations Palermo Catania
"166274.1516"
dragonfly> GEODIST mylocations Palermo Catania km
"166.2742"
dragonfly> GEODIST mylocations Palermo Catania mi
"103.3438"
dragonfly> GEODIST mylocations Palermo Unknown
(nil)
```

## Best Practices

When working with geospatial data, ensure that all required members are added to the geospatial index before attempting to calculate distances between them. Also, choose the appropriate unit for your application's needs to avoid unnecessary conversions.

## Common Mistakes

- **Non-existent Members**: Attempting to calculate the distance between members that do not exist in the geospatial index will result in a `nil` return value.
- **Incorrect Units**: Failing to specify the correct unit can lead to misunderstandings in the results. Always double-check the unit parameter to ensure accuracy.

## FAQs

### What happens if one of the members does not exist?

If either `member1` or `member2` do not exist in the specified geospatial index, the command returns `nil`.

### Can I use GEODIST on non-geospatial data?

No, `GEODIST` is specifically designed for geospatial data managed by `GEOADD`. It cannot be used with other types of data.
