---
description: Learn how to use Redis XADD to append a new entry to a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XADD

<PageTitle title="Redis XADD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XADD` command in Redis is used to add a new entry to a stream. Streams are an abstract data type that allows for the handling of time-series data in a log-like structure. Typical use cases include event logging, message queuing, and real-time analytics.

## Syntax

```plaintext
XADD key ID field value [field value ...]
```

## Parameter Explanations

- **key**: The name of the stream.
- **ID**: The ID of the entry. Use `*` to auto-generate an ID based on the current timestamp.
- **field value**: Pairs of fields and values representing the entry's data. Multiple field-value pairs can be specified.

## Return Values

Returns the ID of the added entry as a string.

### Example Outputs

- `1617844908230-0`: Indicates the entry was successfully added with this specific ID.

## Code Examples

```cli
dragonfly> XADD mystream * sensor-id 1234 temperature 19.8
"1651844970123-0"
dragonfly> XADD mystream 1651844970123-1 sensor-id 1235 temperature 20.1
"1651844970123-1"
dragonfly> XRANGE mystream - +
1) 1) "1651844970123-0"
   2) 1) "sensor-id"
      2) "1234"
      3) "temperature"
      4) "19.8"
2) 1) "1651844970123-1"
   2) 1) "sensor-id"
      2) "1235"
      3) "temperature"
      4) "20.1"
```

## Best Practices

- Use `*` for the ID to ensure uniqueness and avoid conflicts.
- Maintain consistent field naming conventions within streams for easier processing and querying.

## Common Mistakes

- Not specifying the `*` or a valid ID format can lead to errors.
- Forgetting to pair fields and values correctly will result in syntax errors.

## FAQs

### What happens if I use an existing ID?

Redis will not overwrite existing entries; each ID must be unique in the stream.

### Can I add multiple entries at once?

No, `XADD` adds a single entry per command invocation. Use batching techniques on the client-side if necessary.
