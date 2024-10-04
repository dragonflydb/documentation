---
description:  Learn how to manage rate limiting in Redis with CL.THROTTLE command.
---

import PageTitle from '@site/src/components/PageTitle';

# CL.THROTTLE

<PageTitle title="Redis CL.THROTTLE Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `CL.THROTTLE` command is used for rate-limiting actions based on sliding-window counters. 
This command is part of the `redis-cell` module, which enables fine-grained rate limiting without requiring external APIs or complex setups. 
A common use case is limiting user actions, such as the number of API requests made within a certain time window.

## Syntax

```shell
CL.THROTTLE key max-burst tokens-per-interval seconds-per-interval [ignore]
```

## Parameter Explanations

- `key`: The unique identifier for the client or entity whose rate is being limited.
- `max-burst`: The maximum number of tokens that can accumulate in the burst bucket. 
  It allows short-term bursts of actions, beyond a strict limit per second, while still enforcing the overall limit in the long term.
- `tokens-per-interval`: The normal rate of actions allowed within a time window. 
  For example, 10 tokens per minute.
- `seconds-per-interval`: The number of seconds that defines the time window (e.g., allow 10 tokens per 60 seconds).
- `[ignore]` (optional): If provided, this flag permits ignoring the command if it would exceed the `max-burst`. 
  Normally, an action would wait until enough tokens are available.

## Return Values

The `CL.THROTTLE` command returns an array with five elements, providing key information on the current state of the rate limiting system:

1. `integer`: The number of remaining tokens.
2. `integer`: The unique integer indicating how long the client should wait before they can proceed with the next request.
3. `integer`: A flag indicating whether the current request should be allowed (1) or rejected (0).
4. `integer`: The burst bucket size, showing how many tokens can still be stored.
5. `integer`: Time in seconds left until the rate limit is reset.

## Code Examples

### Basic Rate Limiting Example

Consider a rate limit where you allow 5 requests per minute, and the maximum burst allowed is 10 requests. 
Let’s use `CL.THROTTLE` to set this:

```shell
dragonfly> CL.THROTTLE client1 10 5 60
1) (integer) 9  # 9 remaining tokens
2) (integer) 0  # 0 seconds to wait before a next action
3) (integer) 1  # The action is allowed
4) (integer) 10 # Maximum burst size
5) (integer) 60 # Time in seconds for the interval to reset
```

Now let's simulate a client making successive requests within the rate limit:

```shell
# Issuing another request immediately
dragonfly> CL.THROTTLE client1 10 5 60
1) (integer) 8  # 8 remaining tokens
2) (integer) 0  # No wait time
3) (integer) 1  # Action allowed
4) (integer) 10 # Maximum burst size
5) (integer) 60 # Time in seconds for the interval to reset
```

### Example of Exceeding the Rate Limit

Now, let’s send a burst of requests that exceeds the allowable limit:

```shell
# Simulating rapid requests within a second
for i in {1..12}; do dragonfly> CL.THROTTLE client1 10 5 60; done

# After hitting the burst limit and rate threshold
dragonfly> CL.THROTTLE client1 10 5 60
1) (integer) 0    # No remaining tokens
2) (integer) 10   # Wait 10 seconds to proceed with more requests
3) (integer) 0    # Action rejected
4) (integer) 10   # The bucket is full
5) (integer) 60   # Time in seconds for the interval to reset
```

### Using the `ignore` Flag to Bypass Hard Rate Limit Failures

Instead of receiving a rejection when exceeding the rate limit, you can instruct the system to "quietly ignore" excess requests using the `ignore` flag.

```shell
dragonfly> CL.THROTTLE client1 10 5 60 ignore
1) (integer) 0    # No remaining tokens
2) (integer) 0    # No wait since the `ignore` flag was used
3) (integer) 1    # Action "allowed" due to `ignore`
4) (integer) 10   # Maximum burst size
5) (integer) 60   # Time in seconds for the interval to reset
```

Note that while `ignore` prevents full rejections, over time, the client will still be rate-limited based on available tokens.

## Best Practices

- Define rate limits based on real-world usage and assess tolerance for bursts (using `max-burst`) accordingly to ensure application reliability.
- For APIs, it is often useful to return the time left before the client can repeat their request (i.e., value at index 2 of the result).
- The `ignore` flag is useful for scenarios where you want softer rate limiting without outright rejections on excess requests.

## Common Mistakes

- Misunderstanding the difference between `max-burst` and `tokens-per-interval`: 
  The `tokens-per-interval` sets the steady rate, while `max-burst` allows clients to make request bursts up to a limit.
- Assuming that `CL.THROTTLE` is asynchronous: 
  It's not — the checks are immediate, though rejected requests may cause subsequent delays in operation.
  
## FAQs

### What happens if the key does not exist?

When the command is invoked for a new or non-existent key, the counters initialize immediately, starting the tracking with the specified `max-burst` and `tokens-per-interval`.

### Can I use floating-point numbers for `tokens-per-interval`?

No, the `CL.THROTTLE` command currently only supports integer values for `max-burst` and `tokens-per-interval`.

### What is the maximum possible value for `max-burst` and `tokens-per-interval`?

Practically, both `max-burst` and `tokens-per-interval` values are capped by the natural integer limits (2^63 - 1 on 64-bit systems), though operational thresholds may vary depending on your specific use case and performance needs.