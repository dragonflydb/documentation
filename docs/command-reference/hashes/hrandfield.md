---
description: "Learn how to use Redis HRANDFIELD command to get one or more random fields from a hash. Add randomness in your data fetching."
---

import PageTitle from '@site/src/components/PageTitle';

# HRANDFIELD

<PageTitle title="Redis HRANDFIELD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HRANDFIELD` command in Redis is used to retrieve one or more random fields from a hash. It is useful in scenarios where you need to sample field names from a large hash, perform randomized operations, or create a form of load balancing by randomly selecting items.

## Syntax

```plaintext
HRANDFIELD key [count [WITHVALUES]]
```

## Parameter Explanations

- **key**: The name of the hash from which to retrieve the field(s).
- **count** (optional): The number of random fields to retrieve. If not specified, defaults to 1.
- **WITHVALUES** (optional): If specified, the command returns both the field names and their corresponding values.

## Return Values

- If **count** is not specified, it returns a single random field as a bulk string.
- If **count** is specified:
  - Without **WITHVALUES**, it returns an array of fields.
  - With **WITHVALUES**, it returns an array of fields and their respective values.

### Examples:

- Single field: `"field1"`
- Multiple fields: `["field1", "field2"]`
- Fields with values: `["field1", "value1", "field2", "value2"]`

## Code Examples

```cli
dragonfly> HSET myhash field1 "value1" field2 "value2" field3 "value3"
(integer) 3
dragonfly> HRANDFIELD myhash
"field2"
dragonfly> HRANDFIELD myhash 2
1) "field3"
2) "field1"
dragonfly> HRANDFIELD myhash 2 WITHVALUES
1) "field2"
2) "value2"
3) "field1"
4) "value1"
```

## Best Practices

- Use `HRANDFIELD` with caution on very large hashes to avoid performance issues.
- When using the `count` parameter with large values, be aware that there might be duplicates unless the count is less than or equal to the number of fields in the hash.

## Common Mistakes

- Forgetting to specify **WITHVALUES** when both fields and values are needed.
- Assuming the returned fields are unique when the **count** exceeds the total number of fields in the hash.

## FAQs

### What happens if I request more fields than exist in the hash?

If the **count** parameter is greater than the number of fields in the hash, the returned list can contain duplicate fields unless all possible fields have already been returned.

### Can `HRANDFIELD` return the same field multiple times in one call?

Yes, if the **count** is greater than the number of unique fields in the hash, duplicates may occur.
