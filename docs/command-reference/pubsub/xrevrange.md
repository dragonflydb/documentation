---
description: Learn how to use Redis XREVRANGE to fetch a range of messages from a stream in reverse order.
---

import PageTitle from '@site/src/components/PageTitle';

# XREVRANGE

<PageTitle title="Redis XREVRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XREVRANGE` command is used in Redis to fetch entries from a stream data structure in reverse order. It allows you to specify a range of IDs and retrieves the entries from the end of the stream towards the start. This command can be particularly useful when you need to process recent entries first or implement functionalities like reverse pagination.

## Syntax

```plaintext
XREVRANGE <key> <end> <start> [COUNT <count>]
```

## Parameter Explanations

- `<key>`: The name of the stream.
- `<end>`: The maximum ID (inclusive) to start the range from.
- `<start>`: The minimum ID (inclusive) to end the range at.
- `[COUNT <count>]`: Optional. Limits the number of entries returned.

## Return Values

The command returns an array of entries, each entry being another array where the first element is the entry ID and the second element is an array of field-value pairs.

Example:

```plaintext
1) 1) "1609459200010-0"
   2) 1) "field1"
      2) "value1"
2) 1) "1609459199999-0"
   2) 1) "field2"
      2) "value2"
```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1609459200010-0"
dragonfly> XADD mystream * field2 value2
"1609459200020-0"
dragonfly> XREVRANGE mystream + -
1) 1) "1609459200020-0"
   2) 1) "field2"
      2) "value2"
2) 1) "1609459200010-0"
   2) 1) "field1"
      2) "value1"
dragonfly> XREVRANGE mystream 1609459200020-0 1609459200010-0 COUNT 1
1) 1) "1609459200020-0"
   2) 1) "field2"
      2) "value2"
```

## Best Practices

- Use the `COUNT` option to limit the result set size for better performance, especially with large streams.
- Make sure your stream IDs are correctly formatted to avoid unexpected results.

## Common Mistakes

- Incorrectly specifying the order of `<start>` and `<end>` parameters, which can lead to no results.
- Not using the `COUNT` parameter when necessary, potentially leading to fetching too many entries and affecting performance.

## FAQs

### What happens if the `<start>` and `<end>` parameters are reversed?

The command will still work, but it will return an empty array as the range would be invalid.

### Can I use `XREVRANGE` without specifying the `COUNT` parameter?

Yes, the `COUNT` parameter is optional. However, omitting it might lead to very large responses if the stream contains many entries.
