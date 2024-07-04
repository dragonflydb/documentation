---
description: Learn how to manage rate limiting in Redis with CL.THROTTLE command.
---

import PageTitle from '@site/src/components/PageTitle';

# CL.THROTTLE

<PageTitle title="Redis CL.THROTTLE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`CL.THROTTLE` is a command provided by Redis to control the rate of operations on certain keys, effectively implementing a token-bucket algorithm for rate limiting. This is useful in scenarios where you need to limit the number of requests to an API, prevent abuse, or ensure fair usage among clients.

## Syntax

```plaintext
CL.THROTTLE <key> <max_burst> <tokens_per_period> <period>
```

## Parameter Explanations

- `<key>`: The key to which rate limiting will be applied.
- `<max_burst>`: The maximum number of tokens that can be accumulated in the bucket (burst size).
- `<tokens_per_period>`: The number of tokens added to the bucket every period.
- `<period>`: The time period (in milliseconds) after which `tokens_per_period` tokens are added to the bucket.

## Return Values

The command returns an array with five elements:

1. `allowed`: Integer (1 if the action is allowed, 0 otherwise)
2. `remaining_tokens`: Integer (number of tokens left after the current operation)
3. `retry_after`: Integer (time in milliseconds after which the next request can be retried, if not allowed)
4. `reset`: Integer (time in milliseconds until the rate limit resets)
5. `limit`: Integer (maximum number of tokens allowed)

Example output when `CL.THROTTLE mykey 5 1 60000` is executed:

```plaintext
1) (integer) 1
2) (integer) 4
3) (integer) 0
4) (integer) 59999
5) (integer) 5
```

## Code Examples

```cli
dragonfly> CL.THROTTLE api_user_123 10 5 60000
1) (integer) 1
2) (integer) 9
3) (integer) 0
4) (integer) 59999
5) (integer) 10

dragonfly> CL.THROTTLE api_user_123 10 5 60000
1) (integer) 1
2) (integer) 8
3) (integer) 0
4) (integer) 59998
5) (integer) 10

dragonfly> CL.THROTTLE api_user_123 10 5 60000
1) (integer) 0
2) (integer) 0
3) (integer) 2000
4) (integer) 59997
5) (integer) 10
```

## Best Practices

- Adjust `max_burst`, `tokens_per_period`, and `period` values based on your application's traffic patterns and acceptable request limits.
- Monitor the return values to dynamically adjust your rate-limiting strategy as needed.

## Common Mistakes

- Setting `max_burst` or `tokens_per_period` to very low values, which can lead to overly aggressive rate limiting and poor user experience.
- Misinterpreting the `retry_after` value; it indicates the time after which a request can be made again, not immediately after the command is run.

## FAQs

### What happens if I set the period to 0?

Setting the period to 0 will cause the command to return an error since tokens cannot be added in a non-existent timeframe.

### Can `CL.THROTTLE` be used for non-API related rate limiting?

Yes, `CL.THROTTLE` can be used for any scenario requiring rate limiting, such as controlling access to resources or services within an application.
