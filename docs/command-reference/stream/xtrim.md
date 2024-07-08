---
description: Learn how to use Redis XTRIM to limit the length of a stream to a certain size.
---

import PageTitle from '@site/src/components/PageTitle';

# XTRIM

<PageTitle title="Redis XTRIM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XTRIM` command in Redis is used to manage the length of a stream by trimming its entries. This command is particularly useful in scenarios where you need to control memory usage or ensure stream data does not grow indefinitely, such as log processing, event sourcing, or message queues.

## Syntax

```cli
XTRIM <key> MAXLEN [~|=] <count>
```

## Parameter Explanations

- `<key>`: The name of the stream.
- `MAXLEN`: Specifies that the stream will be trimmed based on the maximum length.
- `[~|=]`: (Optional) The `~` argument allows for an approximate trimming (faster but less precise), while `=` means exact trimming.
- `<count>`: The maximum number of entries the stream should hold after trimming.

## Return Values

The `XTRIM` command returns the number of entries removed from the stream.

### Example Outputs

- `(integer) 10`: Indicates that 10 entries were removed from the stream.

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1687351971325-0"
dragonfly> XADD mystream * field1 value2
"1687351971326-0"
dragonfly> XADD mystream * field1 value3
"1687351971327-0"
dragonfly> XLEN mystream
(integer) 3
dragonfly> XTRIM mystream MAXLEN 2
(integer) 1
dragonfly> XLEN mystream
(integer) 2
```

## Best Practices

- Use the `~` option for better performance when exact trimming is not critical.
- Regularly trim streams in applications with high data ingress to prevent excessive memory usage.

## Common Mistakes

- Not specifying `MAXLEN`, which makes the `XTRIM` command invalid.
- Using very low values for `<count>`, potentially causing frequent deletions and impacting performance.

## FAQs

### Can `XTRIM` be used to trim multiple streams at once?

No, `XTRIM` operates on a single stream specified by the `<key>`.

### What happens if I specify `MAXLEN 0`?

Specifying `MAXLEN 0` will trim the stream to have zero entries, effectively clearing it.
