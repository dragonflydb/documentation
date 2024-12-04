---
description: Learn how to use Redis ZSCAN command to incrementally iterate sorted sets elements and associated scores.
---

import PageTitle from '@site/src/components/PageTitle';

# ZSCAN

<PageTitle title="Redis ZSCAN Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZSCAN` command is used to incrementally iterate over the members of a sorted set along with their scores.
This is useful when working with large sorted sets to avoid blocking operations, allowing you to fetch elements in small chunks.

The `ZSCAN` command provides a cursor-based interface to scan through a sorted set, ensuring that only a limited number of elements are returned with each call while redistributing work over multiple client requests.

## Syntax

```shell
ZSCAN key cursor [MATCH pattern] [COUNT count]
```

- **Time complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set to scan.
- `cursor`: This is an opaque string used to iterate through elements. Initially, it must be `0`, and it is updated by the server during each call.
- `MATCH pattern` (optional): An optional glob-style pattern to filter the elements.
- `COUNT count` (optional): With `COUNT`, the user specifies **the amount of work that should be done at every call** in order to retrieve elements from the sorted set.
  **This is just a hint to Dragonfly, and the actual number returned may be different**.

## Return Values

- The command returns an array of two elements:
  - The first element is the new cursor to be used in the next scan. If the returned cursor is `0`, a full iteration is complete.
  - The second element is an array of member-score pairs from the sorted set for this iteration.

## Code Examples

### Basic Example

Scan members from a sorted set using the cursor, starting from `0`:

```shell
dragonfly$> ZADD myzset 10 "a" 20 "b" 30 "c"
(integer) 3

dragonfly$> ZSCAN myzset 0
1) "0"                   # New cursor (0 means full iteration has completed)
2) 1) "a"                # Member
   2) "10"               # Score
   3) "b"                # Member
   4) "20"               # Score
   5) "c"                # Member
   6) "30"               # Score
```

### Scanning with Pattern Matching

Only scan for members whose names match a certain pattern:

```shell
dragonfly$> ZADD myzset 10 "alpha" 20 "beta" 30 "gamma"
(integer) 3

# Scan members whose names start with "a".
dragonfly$> ZSCAN myzset 0 MATCH a*
1) "0"
2) 1) "alpha"
   2) "10"
   
# Scan members whose names contain "a".
dragonfly$> ZSCAN myzset 0 MATCH *a*
1) "0"
2) 1) "alpha"
   2) "10"
   3) "beta"
   4) "20"
   5) "gamma"
   6) "30"
```

### Scanning Continuously Until Data Exhaustion

To fetch all members of a sorted set, the client has to keep scanning with the cursor provided from previous calls:

```shell
# Initialize cursor to 0.
CURSOR="0"

while true; do
  # Fetch members from the sorted set.
  SCAN_RESULT=$(redis-cli ZSCAN myzset $CURSOR COUNT 2)
  
  # Update cursor from server response.
  CURSOR=$(echo "$SCAN_RESULT" | head -n 1)

  # Process members from the server response if needed.
  echo $SCAN_RESULT

  # Break the loop if the returned cursor is back to 0.
  if [ "$CURSOR" -eq "0" ]; then
    break
  fi
done
```

## Best Practices

- Since `ZSCAN` can return the same element more than once during an iteration (due to the nature of the scan mechanism), client-side deduplication may be required if complete accuracy is necessary.
- Use the `MATCH` and `COUNT` options thoughtfully to optimize performance. Increasing the `COUNT` can reduce the total number of round trips but may return larger datasets to process.

## Common Mistakes

- Misinterpreting the returned cursor value. When the returned cursor value is `0`, it indicates that the scan is complete.
- Expecting precise control over the number of elements returned with `COUNT`. It is a hint to the Dragonfly server, but the actual result size may vary.

## FAQs

### Does `ZSCAN` return duplicate elements?

The incremental nature of the `ZSCAN` command implies that it may return the same element more than once over multiple invocations.
It is recommended to handle deduplication on the client-side if it's critical to avoid processing duplicate items.

### Is `ZSCAN` blocking?

No, `ZSCAN` is non-blocking and designed for incrementally iterating through large sets.
It spreads work across multiple calls, preventing performance bottlenecks in a single blocking operation.

### Can I use `ZSCAN` to delete elements?

No, you cannot delete elements from a sorted set using `ZSCAN`.
In the meantime, you should consider if your application logic allows you to delete or modify elements while scanning.
Modifying the sorted set while scanning may result in inconsistent results for your application logic.
