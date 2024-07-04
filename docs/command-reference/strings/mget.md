---
description: Learn how to use Redis MGET to retrieve the values of all specified keys.
---

import PageTitle from '@site/src/components/PageTitle';

# MGET

<PageTitle title="Redis MGET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MGET` command in Redis is used to retrieve the values of multiple keys in a single call. This command is particularly useful when you need to fetch data for several keys simultaneously, which can reduce the number of round-trips between your application and the Redis server, thus improving performance.

## Syntax

```plaintext
MGET key [key ...]
```

## Parameter Explanations

- **key**: One or more keys whose values you want to retrieve. If a key does not exist, its corresponding value in the output will be `nil`.

## Return Values

The `MGET` command returns an array of values corresponding to the specified keys. If a key does not exist, its position in the array will contain `nil`. For example:

```cli
dragonfly> MGET key1 key2 key3
1) "value1"
2) nil
3) "value3"
```

## Code Examples

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> SET key3 "value3"
OK
dragonfly> MGET key1 key2 key3
1) "value1"
2) nil
3) "value3"
```

## Best Practices

- When retrieving values for a known set of keys, use `MGET` instead of multiple `GET` commands to minimize latency.
- If you are working with a large number of keys, ensure that the payload size returned by `MGET` is manageable to avoid potential performance issues.

## Common Mistakes

- Using `MGET` with non-existing keys expecting all results to be non-`nil` can lead to confusion. Always handle `nil` values appropriately in your application logic.

## FAQs

### Can I use MGET with a mix of existing and non-existing keys?

Yes, `MGET` will return `nil` for any keys that do not exist.

### Is there a limit to the number of keys I can specify with MGET?

There is no explicit limit imposed by Redis; however, practical limits may be dictated by network bandwidth and client memory constraints.
