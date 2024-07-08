---
description: Learn how to use Redis XADD to append a new entry to a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XADD

<PageTitle title="Redis XADD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XADD` command in Redis is used to append a new entry to a stream. Streams are a type of data structure that allows for the storage of an ordered log of messages, making them particularly useful for messaging systems, event sourcing, and logging applications.

## Syntax

```cli
XADD key ID field value [field value ...]
```

## Parameter Explanations

- **key**: The name of the stream.
- **ID**: The unique identifier for the entry. It can be specified as `*` to let Redis generate a timestamp-based ID.
- **field value**: Pairs of field names and values to store in the entry. At least one field-value pair must be provided.

## Return Values

The command returns the ID of the added entry.

### Example Outputs

- When a new entry is added successfully:
  ```cli
  dragonfly> XADD mystream * sensor-id 1234 temperature 19.8
  "1633389163432-0"
  ```

## Code Examples

```cli
dragonfly> XADD mystream * sensor-id 1234 temperature 19.8
"1633389163432-0"
dragonfly> XADD mystream 1633389163432-1 sensor-id 5678 temperature 22.5
"1633389163432-1"
dragonfly> XLEN mystream
(integer) 2
dragonfly> XRANGE mystream - +
1) 1) "1633389163432-0"
   2) 1) "sensor-id"
      2) "1234"
      3) "temperature"
      4) "19.8"
2) 1) "1633389163432-1"
   2) 1) "sensor-id"
      2) "5678"
      3) "temperature"
      4) "22.5"
```

## Best Practices

- Use meaningful IDs instead of relying on automatic generation, if the time sequence or specific ordering is critical.
- Regularly trim your streams using the `XTRIM` command to maintain manageable sizes and performance.

## Common Mistakes

- Forgetting to provide at least one field-value pair will result in an error.
- Using non-unique IDs can cause unexpected behavior, so ensure that IDs are unique if manually specified.

## FAQs

### What happens if I use the same ID for multiple entries?

Using the same ID for multiple entries can lead to overwriting or unexpected behavior. It's best to ensure each ID is unique.

### Can I have an empty stream?

No, streams require at least one entry. Attempting to create an empty stream will result in an error.
