---
sidebar_position: 1
description: Relay
---

# Relay

**Notes:**

- Dragonfly v1.14+ and the [RESP3](https://github.com/redis/redis-specifications/blob/master/protocol/RESP3.md) protocol are required for this integration.
- See more details about the [`CLIENT TRACKING`](../command-reference/server-management/client-tracking.md) command that enables this integration.

## Introduction

[Relay](https://relay.so/) is a revolutionary PHP extension that combines the functionalities of a Redis client
with an advanced shared in-memory cache, offering exceptional caching performance enhancements.

Relay can be used as a drop-in replacement for [phpredis](https://github.com/phpredis/phpredis).
By maintaining a highly-efficient partial replica of Redis data in the PHP master process memory and utilizing real-time cache invalidation and updates, Relay significantly outperforms traditional clients.
Tailored for shared environments, it allows for precise memory management, employing LRU and LFU eviction policies to optimize performance.
Relay supports seamless integration across major platforms like Laravel, WordPress, Magento, and Drupal without requiring code modifications.

Dragonfly is highly compatible with Redis, and Relay can be effortlessly used with Dragonfly (v1.14+) with
[even better performance and efficiency](https://www.dragonflydb.io/blog/relay-with-dragonfly-towards-the-next-gen-caching-infrastructure).

## Using Relay with Dragonfly

### 1. Dragonfly Initialization

There are several options available to [get Dragonfly up and running quickly](../getting-started/getting-started.md).
Assuming you have a local Dragonfly binary, you can run Dragonfly with the following command:

```bash
$> ./dragonfly --bind localhost --port 6379
```

### 2. Relay Installation

For different platforms, you can install Relay by following the instructions in their [documentation](https://relay.so/docs/installation).

### 3. Start Using Relay with Dragonfly

Once you have Dragonfly and Relay set up, you can start using Relay with Dragonfly in code.
For more information on how to use Relay in terms of configuration, integrations, events, and APIs, please refer to the Relay [documentation](https://relay.so/docs).

<!-- PHP is not supported for syntax highlighting yet, and the JavaScript highlighting looks fine for this example. -->
```javascript
// Assume Dragonfly is running locally on the default port.
$relay = new Relay(host: '127.0.0.1', port: 6379);

// Fetch the user count from Relay's memory, or from Dragonfly if the key has not been cached, yet.
$users = $relay->get('users:count');

// Listen to all invalidation events.
$relay->onInvalidated(function (Relay\Event $event) use ($users) {
    if ($event->key === 'users:count') {
        $users = null;
    }
});
```

## Useful Resources & Benchmarks

- Relay [Homepage](https://relay.so/), [GitHub](https://github.com/cachewerk/relay), and [Documentation](https://relay.so/docs).
- Read our blog post [Relay with Dragonfly: Towards the Next-Gen Caching Infrastructure](https://www.dragonflydb.io/blog/relay-with-dragonfly-towards-the-next-gen-caching-infrastructure)
  with internal implementation details and performance benchmarks.
