---
sidebar_position: 2
---

# Frequently Asked Questions

## What is the licensing model for Dragonfly? Is it open source?
Dragonfly is released under [BSL 1.1](../LICENSE.md) (Business Source License). We believe that a BSL license is more permissive than AGPL-like licenses. In general terms, it means that dragonfly's code is free to use and free to change as long as you do not sell services directly related to dragonfly or in-memory datastores.
We followed the model set by other companies like Elastic, Redis, MongoDB, Cockroach labs, Redpanda Data to protect our rights to provide service and support for the software we are building. 

## Can I use dragonfly in production?
License wise you are free to use dragonfly in production as long as you do not provide dragonfly as a managed service. If you would like help from the DragonflyDB team in getting up and runnning, you may apply for our [free Early Access Program](https://dragonflydb.io/early-access).

## How does Dragonfly's vertical scaling compare to a Redis cluster?
Dragonfly utilizes the underlying hardware in an optimal way. This means that it can run on small 8GB instances and scale verticly to large 768GB machines with 64 cores. This versatility allows for a far less complexity as well as lower infrastructure costs when compared to running cluster workloads. In addition, Redis cluster-mode imposes some limitations on multi-key and transactinal operations while Dragonfly provides the same semantics as single node Redis.

## When will you support X command?
Dragonfly has implemented ~150 Redis commands which we think represents good coverage for the vast majority of use cases. Having said that, if you require commands that are not supported, please feel free to open an issue or vote on an existing issue. We will do our best to prioritise those commands according to their popularity.
