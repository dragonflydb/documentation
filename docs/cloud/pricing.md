---
sidebar_position: 10
---

# Pricing

## Overview

Dragonfly Cloud applies a transparent usage-based pricing model with the following components:

- [Active Data Stores](#active-data-stores)
- [Data Transfer](#data-transfer)
- [Backup Storage](#backup-storage)

You can track your usage and costs under the [Account > Usage](https://dragonflydb.cloud/account/usage) tab in Dragonfly Cloud.
The usage and cost information is updated every few hours.
However, data transfer and backup storage costs may take up to 24 hours to reflect.
Read on for more details about each component.

## Active Data Stores

Data stores incur charges for **every prorated hour they are active**.
The cost is determined by:

- **Provisioned Memory Amount** (All Primary & Replica Instances)
- **Compute Performance Tier**
- **Cloud Provider & Region**

Additional notes about data store costs:

- Updating a data store configuration only affects its cost once the update is complete and the new configuration is active.
- Deleted data stores do not incur any charges.

### Example: Data Store Cost Calculation

To illustrate with an example, let's consider a Dragonfly Cloud data store that is:

- Configured with **12.5GB** of provisioned memory on the **enhanced performance tier**.
- Configured with **2 zones**, one primary and one replica.
- Located in the **AWS us-east-1** region.
- Active for **2 days, 1 hour, and 10 minutes**.

The cost of this data store can be calculated as follows:

- Cost for 1GB of enhanced performance tier data store in AWS us-east-1: around $11.0 per month.
- Total hours used: 2 days x 24 hours per day + 1 hour + 10 minutes (rounded up to 1 hour) = 50 hours.
- Total hours in a month: 365 days / 12 months x 24 hours per day = 730 hours per month.
- Total cost: **$11 x 12.5GB x 2 zones x 50 hours / 730 hours per month = $18.84**

## Data Transfer

- Data transfer fees are costs imposed by cloud providers for moving data across various destinations,
  including between clouds, the public internet, different cloud regions, and even between availability zones within the same region.
- Dragonfly Cloud applies public data transfer fee rates set by cloud vendors for data store traffic.
  For detailed and specific pricing, please refer to the [AWS](https://aws.amazon.com/ec2/pricing/on-demand/) and [GCP](https://cloud.google.com/vpc/network-pricing) pages.
- **To reduce data transfer expenses, using [data stores with private endpoints](./datastores.md#private-endpoint) is recommended**.
- Additionally, data stores with high-availability configured may incur charges for cross-availability zone traffic within the cloud provider's network.

## Backup Storage

- Backup storage costs $0.1 per GB per month, prorated hourly.
