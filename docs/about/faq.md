---
description: "Answers to frequently asked questions about Dragonfly's licensing, production readiness, scaling, and command support."
sidebar_position: 2
---

# Frequently Asked Questions

## What is the licensing model for Dragonfly? Is it open source?

Starting with v2.1, Dragonfly is released as Dragonfly Enterprise under the [Dragonfly Source-Available License (DSAL)](https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md). Dragonfly Enterprise is the continuation of Dragonfly: the same codebase, built by the same team. DSAL is a "source available" license and it's not strictly an open-source license. In general terms, it means that Dragonfly's code is free to use, modify and incorporate into your own applications or products, as long as you do not distribute or offer it as a standalone database, data store, caching product or a substantially similar product or service. Production use is free up to an aggregate of 100 vCPUs across all your concurrently running instances (including replicas), while non-production use is unlimited. Usage beyond that requires a commercial license.
We followed the model set by other companies like Elastic, Redis, MongoDB, Cockroach labs, Redpanda Data to protect our rights to provide service and support for the software we are building.

Releases before v2.1 remain under BSL 1.1 (Business Source License), with the terms in the `LICENSE.md` file of each release, for example [v2.0.0](https://github.com/dragonflydb/dragonfly/blob/v2.0.0/LICENSE.md).

## Can I use Dragonfly in production?

Yes, Dragonfly is built for production and has seen massive adoption across demanding, data-intensive environments. Under the DSAL, which applies to Dragonfly Enterprise (v2.1 and later), you are free to self-host it in production up to an aggregate of 100 vCPUs across all your concurrently running instances (including replicas), as long as you do not provide it as a standalone database, data store or caching product or service. Beyond that, you need a commercial license: to get one, sign up at [dragonflydb.cloud](https://dragonflydb.cloud/signup). See the [LICENSE](https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md) for the exact terms.

For teams that want out-of-the-box scaling, security, and expert support, we launched **[Dragonfly Cloud](https://www.dragonflydb.io/cloud)** - the easiest and most reliable way to run Dragonfly in production.

## How does Dragonfly's vertical scaling compare to a Redis cluster?

Dragonfly utilizes the underlying hardware in an optimal way. This means that it can run on small 8GB instances and scale vertically to the largest multi-terabyte machines. This versatility allows for far less complexity as well as lower infrastructure costs when compared to running cluster workloads. In addition, Redis cluster-mode imposes some limitations on multi-key and transactional operations while Dragonfly provides the same semantics as a single node Redis.

## When will you support X command?

You can check our [command reference](../category/command-reference) pages to see which commands are already supported.
Dragonfly has implemented more than 200 Redis commands which we think represents good coverage
for the vast majority of use cases. Having said that, if you require commands that are not supported,
please feel free to open an issue or vote on an existing issue.
We will do our best to prioritise those commands according to their popularity.
