---
description: "Discover how to use Redis SCAN command for incremental iteration over a collection of keys."
---

import PageTitle from '@site/src/components/PageTitle';

# SCAN

<PageTitle title="Redis SCAN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCAN` command in Redis is used to incrementally iterate over a collection of elements, such as keys in the current database or elements in a hash, set, sorted set, or list. It allows for scanning large datasets without blocking the server for a long time. Typical scenarios include iterating through all keys in a database, fetching members of a set, or retrieving fields in a hash.

## Syntax

```plaintext
SCAN cursor [MATCH pattern] [COUNT count]
```

## Parameter Explanations

- **cursor**: This is an integer that represents the iteration state. The first call should start with 0, and subsequent calls should use the cursor returned by the previous `SCAN` call.
- **MATCH pattern**: (Optional) A pattern to filter the keys. For example, `MATCH user:*` will return only keys that start with "user:".
- **COUNT count**: (Optional) A hint to the server about how many elements to return in this scan. The default is 10.

## Return Values

The `SCAN` command returns an array with two elements:

1. **Cursor**: An integer to be used as the cursor in the next call.
2. **Elements**: An array of elements (keys, fields, etc.) retrieved in this scan iteration.

### Example Outputs

```plaintext
1) "42"
2) 1) "key1"
   2) "key2"
   3) "key3"
```

In the above example, "42" is the cursor for the next call, and "key1", "key2", and "key3" are the elements found in this scan iteration.

## Code Examples

```cli
dragonfly> SCAN 0
1) "4"
2) 1) "key1"
   2) "key2"
dragonfly> SCAN 4 MATCH user:*
1) "0"
2) 1) "user:1000"
   2) "user:1001"
dragonfly> SCAN 0 COUNT 5
1) "12"
2) 1) "key1"
   2) "key2"
   3) "key3"
   4) "key4"
   5) "key5"
```

## Best Practices

- Use the `MATCH` option to filter results and reduce unnecessary data transfer.
- Adjust the `COUNT` option based on your application's performance requirements and available memory to balance between speed and resource usage.

## Common Mistakes

- Not using the returned cursor correctly can result in incomplete scans or repeated data.
- Assuming `SCAN` guarantees a specific number of elements per call; it's just a hint, not a strict count.

## FAQs

### What is the difference between `SCAN` and `KEYS`?

`KEYS` retrieves all matching keys at once and can block the server if the dataset is large. `SCAN` fetches keys incrementally, making it more suitable for large datasets.

### Can I use `SCAN` to delete keys?

Yes, you can use `SCAN` in combination with `DEL` to delete keys in batches without blocking the server.
