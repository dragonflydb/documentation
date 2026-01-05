---
sidebar_position: 1
description: django-cacheops
---

# django-cacheops

## Introduction

[django-cacheops](https://github.com/Suor/django-cacheops) is a slick ORM cache for Django with automatic granular event-driven invalidation.
It provides intelligent caching for Django applications with both manual and automatic capabilities, using Redis as its backend storage system.

Key features include:
- Automatic caching of Django ORM queries
- Granular cache invalidation based on database events
- Decorators to cache user functions and views
- Dog-pile prevention mechanisms
- Template extensions for Django and Jinja2

Dragonfly is highly compatible with Redis, and django-cacheops can be used with Dragonfly.
By replacing Redis with Dragonfly, you can achieve superior performance and memory efficiency for your Django application's caching layer.

## TL;DR

Dragonfly includes built-in support for django-cacheops scripts.
In most cases, **django-cacheops works with Dragonfly out of the box** without any additional configuration.

If you encounter errors related to undeclared keys, run Dragonfly with the following flag:

```bash
./dragonfly --default_lua_flags=allow-undeclared-keys
```

That's all you need to know to run django-cacheops with Dragonfly.
If you want to learn more about the technical details, please continue reading the sections below.

---

## Technical Background

### Why Undeclared Keys?

django-cacheops uses Lua scripts for cache operations and invalidation.
These scripts dynamically construct cache keys at runtime based on query parameters and table relationships.
For example, the caching script builds conjunction keys like:

```
{prefix}conj:{db_table}:{field}={value}&{field2}={value2}
```

These keys are not passed in the `KEYS` array but are constructed inside the Lua script from `ARGV` data.
While Redis allows this pattern (though it's technically unsupported), Dragonfly by default requires all accessed keys to be declared upfront for optimal multi-threaded performance.

### Built-in Script Recognition

Dragonfly automatically recognizes the SHA signatures of django-cacheops Lua scripts and enables undeclared key access for them.
This means that standard django-cacheops installations should work without any configuration changes.

## Configuration Options

If the automatic script recognition doesn't cover your use case (e.g., you're using a modified version of django-cacheops or a newer version with different scripts), you have several options:

### Option 1: Default Lua Flags (Recommended)

Run Dragonfly with the `allow-undeclared-keys` flag applied to all scripts:

```bash
./dragonfly --default_lua_flags=allow-undeclared-keys
```

**Note:** This option allows any Lua script to access undeclared keys, which requires Dragonfly to use global locking during script execution.
This may impact performance for workloads with many concurrent Lua scripts.

### Option 2: Script-Specific Flags

If you know the SHA of the specific scripts that need undeclared key access, you can configure them individually using the `SCRIPT FLAGS` command:

```bash
# First, identify the SHAs used by your application
127.0.0.1:6379> SCRIPT LIST

# Then, set the flag for specific scripts
127.0.0.1:6379> SCRIPT FLAGS <sha1> allow-undeclared-keys
```

This command can be called **before the script is loaded**, making it possible to pre-configure scripts before starting your Django application.

### Option 3: Custom SHA List

You can also provide a list of SHAs that should allow undeclared keys via a startup flag:

```bash
./dragonfly --lua_undeclared_keys_shas=sha1,sha2,sha3
```

## Django Configuration

Configure django-cacheops to connect to Dragonfly by updating your Django settings.
Since Dragonfly is Redis-compatible, you can use the same configuration format:

```python
# settings.py

CACHEOPS_REDIS = {
    'host': 'localhost',  # Dragonfly host
    'port': 6379,         # Dragonfly port
    'db': 0,
}

# Or using a URL
CACHEOPS_REDIS = "redis://localhost:6379/0"

# Configure caching rules for your models
CACHEOPS = {
    # Cache all User model queries for 15 minutes
    'auth.user': {'ops': 'all', 'timeout': 60*15},

    # Cache gets and fetches for Profile model
    'myapp.profile': {'ops': ('get', 'fetch'), 'timeout': 60*60},

    # Cache all operations for all models in myapp
    'myapp.*': {'ops': 'all', 'timeout': 60*10},

    # Default for all other models
    '*.*': {'ops': (), 'timeout': 60*5},
}

# Optional: Enable graceful degradation if Dragonfly is unavailable
CACHEOPS_DEGRADE_ON_FAILURE = True
```

## Performance Considerations

When using `allow-undeclared-keys`, Dragonfly operates in global mode during Lua script execution, which serializes script operations.
For most django-cacheops workloads, this has minimal impact because:

1. Cache operations are typically short-lived
2. The performance benefit of caching far outweighs the serialization overhead
3. Dragonfly's efficient memory management provides benefits beyond raw throughput

If you have a write-heavy workload with many concurrent cache invalidations, consider:

- Batching database operations to reduce invalidation frequency
- Using `CACHEOPS_DEGRADE_ON_FAILURE = True` for resilience
- Monitoring cache hit rates to ensure caching is effective

## Useful Resources

- django-cacheops [GitHub](https://github.com/Suor/django-cacheops) and [Documentation](https://github.com/Suor/django-cacheops#readme)
- Dragonfly [Scripting with Lua](../managing-dragonfly/scripting.md) documentation
- Django [Caching Framework](https://docs.djangoproject.com/en/stable/topics/cache/) documentation
