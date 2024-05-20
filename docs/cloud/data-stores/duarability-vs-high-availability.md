---
sidebar_position: 3
title: Durability and Availability
--- 


# Durability and Availability
Dragonfly Cloud prioritizes both data durability and high availability for your data stores. You can further fine-tune these aspects through the concept of eviction policies when creating a data store. This allows you to strike a balance between data persistence and performance based on your application's needs.


## Eviction Policies

Eviction policies determine how Dragonfly Cloud manages data storage capacity within your data store. Here's an explanation of the available options:

- **Cache**: The "Cache" eviction policy treats your DragonFly data store as a cache. When the data store reaches its capacity limit, items are evicted to free up space. This policy is useful for caching scenarios where occasional data loss is acceptable.

- **No Eviction**: The "No Eviction" policy ensures that data stored in your DragonFly data store is never evicted. Instead, when the data store reaches its capacity limit, it will return an error. This policy is useful for scenarios that require persistent storage, where data loss is unacceptable.






