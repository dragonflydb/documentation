---
sidebar_position: 3
---

import PageTitle from '@site/src/components/PageTitle';

# Dragonfly Cloud Enterprise

<PageTitle title="Enterprise | Dragonfly Cloud" />

## Overview

**Dragonfly Cloud Enterprise** is a fully managed service designed for organizations that require extremely high-performance in-memory data stores at scale. It is suited for use cases involving:

- **Large-Scale Data**: Datasets from over **500GB** to multiple terabytes.
- **Extreme Throughput**: **Millions of requests per second (RPS)** with low latency.
- **High Availability**: **99.99% uptime** with robust failover and multi-region backups.
- **Automatic Scalability**: Intelligent **auto-scaling** capabilities adapt to dynamic traffic patterns.
- **Security and Compliance**: Advanced security controls and **deployments on your existing cloud servers (BYOC)**.

Dragonfly Cloud Enterprise offers everything in Dragonfly Cloud plus the following enhancements and guarantees.
If you are interested in Dragonfly Cloud Enterprise, please [contact us](https://www.dragonflydb.io/enterprise)
to start a proof-of-concept.

---

## Scalability and Performance

### Dragonfly Swarm

At the heart of Dragonfly Cloud Enterprise is [Dragonfly Swarm](./datastores#dragonfly-swarm-multi-shard),
which enables horizontal scalability on top of Dragonfly's advanced multi-threaded architecture.
It first maximizes the resources of a single instance, which can utilize all available CPU cores
and scale vertically to support up to 600GB of memory and millions of requests per second.
When further scale is required, the system can seamlessly add nodes to form a **distributed multi-shard cluster**
capable of handling **hundreds of terabytes of memory and hundreds of millions of requests per second (RPS)**.

### Read Replicas

For read-intensive applications, the service provides [read replicas](./connect/redis-clients.md).
These replicas distribute read traffic across multiple instances to reduce latency and increase the overall throughput even further.

---

## Flexibility and Cost Efficiency

### Auto-Scaling

Dragonfly Cloud Enterprise includes an auto-scaling feature that **dynamically adjusts resources** in response to traffic fluctuations,
**without any manual intervention**. This helps maintain performance during demand spikes and optimize efficiency during quieter periods.
Scaling policies can be customized to align with specific workload patterns.

### Bring-Your-Own-Cloud (BYOC) \[Beta\]

The BYOC option of Dragonfly Cloud Enterprise can
**deploy fully managed Dragonfly data stores directly within your cloud account (AWS, GCP, or Azure)**.
This model enhances security and compliance by keeping all data within your controlled environment.
It can also provide cost benefits by utilizing your existing cloud servers.

### Guaranteed 30% Lower Costs

Dragonfly Cloud Enterprise is designed to offer significant cost efficiency.
It provides a pricing structure that typically results in much lower costs compared to other cloud in-memory data services.
For Dragonfly Cloud Enterprise, we guarantee [at least 30% cost savings](https://www.dragonflydb.io/pricing)
compared to your current managed in-memory data store solution.

---

## Reliability and Support

### Multi-Region Backups

Data durability is provided through multi-region backups.
Critical data is replicated and stored across geographically diverse locations to
ensure resilience and speedy recovery in the event of a regional outage.

### Premium Enhanced Support

Enterprise includes direct support from the engineers who built Dragonfly.
This provides assistance for onboarding, configuration, and ongoing operations.
**Expert support is available 24/7**.

---

## Getting Started

Dragonfly Cloud Enterprise is designed to meet the demands of modern enterprise workloads,
providing extremely high scale, performance, and cost efficiency.

To evaluate the service for your use case, [contact us](https://www.dragonflydb.io/enterprise) to begin a proof-of-concept.
