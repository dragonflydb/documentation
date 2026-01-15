---
sidebar_position: 1
description: Magento (Adobe Commerce)
---

# Magento

## Introduction

[Magento](https://business.adobe.com/products/magento/open-source.html) (also known as Adobe Commerce) is a powerful open-source e-commerce platform written in PHP.
It powers thousands of online stores worldwide and requires a fast in-memory data store for optimal performance.

Magento relies on an in-memory store for three critical functions:

- **Default Cache**: Application-level caching for configurations, layouts, and block HTML output.
- **Page Cache (Full Page Cache)**: Stores complete rendered pages for ultra-fast delivery to visitors.
- **Session Storage**: Manages user sessions for shopping carts, authentication, and checkout flows.

Dragonfly integrates seamlessly with Magento, providing high-throughput caching and session management.
By using Dragonfly, you can achieve superior performance and memory efficiency for your Magento store,
especially under high traffic loads during peak shopping periods.

## TL;DR

Dragonfly works with Magento out of the box. Configure your Magento installation to connect to Dragonfly using the standard protocol,
and your store will benefit from Dragonfly's multi-threaded architecture and efficient memory management.

A complete Docker-based example is available in the
[dragonfly-examples](https://github.com/dragonflydb/dragonfly-examples/tree/main/magento-integration) repository.

---

## Running Magento with Dragonfly

### 1. Dragonfly Initialization

There are several options available to [get Dragonfly up and running quickly](../getting-started/getting-started.md).
For production environments, ensure Dragonfly is accessible from your Magento application servers.

```bash
# Run Dragonfly with default settings
$> ./dragonfly --bind 0.0.0.0 --port 6379
```

For high-traffic Magento stores, consider enabling memory limits and persistence:

```bash
$> ./dragonfly --bind 0.0.0.0 --port 6379 --maxmemory 4gb --dbfilename dump.rdb
```

### 2. Magento Configuration

Magento stores its backend configuration in `app/etc/env.php`.
Configure Dragonfly as the backend for cache and sessions by updating this file:

```php
<?php
return [
    // ... other configuration ...

    'cache' => [
        'frontend' => [
            'default' => [
                'id_prefix' => 'MAGENTO_CACHE_',
                'backend' => 'Magento\\Framework\\Cache\\Backend\\RemoteSynchronizedCache',
                'backend_options' => [
                    'remote_backend' => 'Cm_Cache_Backend_Redis',
                    'remote_backend_options' => [
                        'server' => 'dragonfly.host',  // Your Dragonfly host
                        'port' => '6379',
                        'database' => '0'
                    ],
                    'local_backend' => 'Cm_Cache_Backend_File',
                    'local_backend_options' => [
                        'cache_dir' => '/var/www/html/magento/var/cache'
                    ]
                ]
            ],
            'page_cache' => [
                'id_prefix' => 'MAGENTO_PAGE_CACHE_',
                'backend' => 'Cm_Cache_Backend_Redis',
                'backend_options' => [
                    'server' => 'dragonfly.host',  // Your Dragonfly host
                    'port' => '6379',
                    'database' => '1'
                ]
            ]
        ]
    ],

    'session' => [
        'save' => 'redis',
        'redis' => [
            'host' => 'dragonfly.host',  // Your Dragonfly host
            'port' => '6379',
            'database' => '2',
            'timeout' => '2.5',
            'persistent_identifier' => '',
            'compression_threshold' => '2048',
            'compression_library' => 'gzip',
            'max_concurrency' => '6',
            'break_after_frontend' => '5',
            'break_after_adminhtml' => '30'
        ]
    ],

    // ... other configuration ...
];
```

Alternatively, use the Magento CLI to configure Dragonfly during installation or updates:

```bash
php bin/magento setup:config:set \
  --cache-backend=redis \
  --cache-backend-redis-server=dragonfly.host \
  --cache-backend-redis-db=0 \
  --page-cache=redis \
  --page-cache-redis-server=dragonfly.host \
  --page-cache-redis-db=1 \
  --session-save=redis \
  --session-save-redis-host=dragonfly.host \
  --session-save-redis-db=2
```

### 3. Database Separation

Using separate databases for different cache types is recommended:

| Cache Type | Database | Purpose |
|------------|----------|---------|
| Default Cache | db=0 | Application cache, configurations, layouts |
| Page Cache | db=1 | Full page cache for faster page loads |
| Sessions | db=2 | User sessions, shopping carts, authentication |

This separation allows for independent cache management.
For example, you can flush the page cache without affecting user sessions.

### 4. Cache Management

After configuration, flush the Magento cache to ensure the new settings take effect:

```bash
# Flush all caches
php bin/magento cache:flush

# Verify cache status
php bin/magento cache:status
```

## Docker Example

A complete Docker Compose setup with Magento 2.4.8, MySQL, OpenSearch, and Dragonfly is available in the
[dragonfly-examples](https://github.com/dragonflydb/dragonfly-examples/tree/main/magento-integration) repository.

The example includes:

- Pre-configured Docker services for a complete Magento development environment
- Automated installation script with Dragonfly configuration
- Sample data setup for testing
- Testing scripts

Quick start:

```bash
git clone https://github.com/dragonflydb/dragonfly-examples.git
cd dragonfly-examples/magento-integration
cp .env.example .env
# Edit .env with your Dragonfly IP and Magento Marketplace credentials
docker compose up -d
```

## Performance Considerations

For optimal Magento performance with Dragonfly:

1. **Memory Allocation**: Allocate sufficient memory for your cache workload. A typical Magento store with moderate traffic benefits from 2-4GB dedicated to caching.

2. **Connection Pooling**: Magento's session configuration supports connection settings like `max_concurrency` and timeout values. Tune these based on your traffic patterns.

3. **Cache Warming**: After deployment or cache flush, consider warming the cache by crawling key pages to pre-populate the page cache.

4. **Monitoring**: Monitor Dragonfly's memory usage and hit rates to ensure optimal cache utilization.

## Useful Resources

- Magento Open Source [Homepage](https://business.adobe.com/products/magento/open-source.html) and [Documentation](https://developer.adobe.com/commerce/docs/).
- Complete Docker example in the [dragonfly-examples](https://github.com/dragonflydb/dragonfly-examples/tree/main/magento-integration) repository.
- Dragonfly [Getting Started](../getting-started/getting-started.md) guide.
- For PHP applications, also see the [Relay](./relay.md) integration for enhanced in-memory caching.
