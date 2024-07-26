---
description: Learn how to manage rate limiting in Redis with CL.THROTTLE command.
---

import PageTitle from '@site/src/components/PageTitle';

# CL.THROTTLE

<PageTitle title="Redis CL.THROTTLE Explained (Better Than Official Docs)" />

## Introduction

The `CL.THROTTLE` command in Redis is used for rate limiting. It helps to control the rate of requests or actions, ensuring that they do not exceed a specified threshold over a given period. This is particularly useful for implementing API rate limits, protecting resources from abuse, and managing traffic bursts.

## Syntax

```plaintext
CL.THROTTLE key max_burst tokens_per_period period duration
```

## Parameter Explanations

- **key**: The unique identifier for the rate limiter instance.
- **max_burst**: The maximum number of tokens that can be accumulated.
- **tokens_per_period**: Number of tokens added to the bucket at each period.
- **period**: The interval at which tokens are added.
- **duration**: The time window for rate limiting.

## Return Values

The `CL.THROTTLE` command returns an array containing five elements:

1. A status code (0 for allowed, 1 for denied).
2. The current number of tokens available.
3. The number of tokens requested.
4. The total number of tokens in the bucket.
5. The time to wait before the next token is available (in milliseconds).

### Example Output

```plaintext
[0, 9, 1, 10, 0]
```

## Code Examples

### Basic Example

```cli
dragonfly> CL.THROTTLE mylimiter 15 5 60 1
1) (integer) 0
2) (integer) 14
3) (integer) 1
4) (integer) 15
5) (integer) 0
```

### Rate Limiting API Requests

This example shows how to use `CL.THROTTLE` to limit API requests to 10 per minute.

```cli
dragonfly> CL.THROTTLE api_rate_limiter 10 1 60 1
1) (integer) 0
2) (integer) 9
3) (integer) 1
4) (integer) 10
5) (integer) 0
```

### Controlling Login Attempts

This example limits login attempts to 5 per hour to prevent brute force attacks.

```cli
dragonfly> CL.THROTTLE login_attempts 5 1 3600 1
1) (integer) 0
2) (integer) 4
3) (integer) 1
4) (integer) 5
5) (integer) 0
```

## Best Practices

- Choose appropriate values for `max_burst` and `tokens_per_period` based on your specific use case requirements.
- Monitor and adjust the rate limits according to the observed traffic patterns and application load.

## Common Mistakes

- Setting `tokens_per_period` too high or low, leading to either excessive throttling or insufficient protection against abuse.
- Not considering the cumulative effect of multiple rate-limited actions, which can lead to unexpected behavior.

## FAQs

### What happens if the bucket runs out of tokens?

The request will be denied, and the return value will indicate a wait time before the next token becomes available.

### Can I use different rate limits for different actions?

Yes, you can create separate keys with their own rate limits for different actions or endpoints.
