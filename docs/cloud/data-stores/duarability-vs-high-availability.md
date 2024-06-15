---
sidebar_position: 3
title: Durability and Availability
--- 


## Eviction Policies

Eviction policy controls the behavior of the datastore when it maxes out its memory.

No Eviction - Items are never evicted and out of memory errors are returned when the data store is full.

 
Cache - The data store behaves as cache and evicts items to free space for new ones when the data store is full.


## High Availability

By default the data store will consist of a single Dragonfly server, this means that in case of software failures,  hardware failures or cloud zone outages data is lost and the data store may be completely unavailable.

To increase availability of your data store you can select up to two replicas in different zones in the High Availability drop down.
The data store master node will be placed in the primary availability zone.
To avoid data transfer costs incurred by the cloud provider, select the primary availability zone to match the availability zone of your application. 





