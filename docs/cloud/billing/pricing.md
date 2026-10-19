---
description: "Dragonfly Cloud's usage-based pricing model for active data stores, data transfer."
sidebar_position: 1
slug: /cloud/pricing
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from '@site/src/components/CloudBadge/CloudBadge'

# Pricing
<CloudBadge/>
<PageTitle title="Pricing | Dragonfly Cloud" />

## Overview

Dragonfly Cloud applies a transparent usage-based pricing model with the following components:

- [Overview](#overview)
- [Price Summary](#price-summary)
- [Active Data Stores](#active-data-stores)
  - [Active Data Store Cost Calculation](#active-data-store-cost-calculation)
  - [Active Data Store Cost Example](#active-data-store-cost-example)
- [Data Transfer](#data-transfer)

See [Payment Methods](./payment-methods.md) for the ways to pay, including credit card and AWS, GCP, and Azure Marketplace.

You can track your usage and costs under the [Account > Usage](https://dragonflydb.cloud/account/usage) tab
in Dragonfly Cloud. The usage and cost information is updated every few hours.
However, data transfer may take up to 24 hours to reflect.
Read on for more details about each component.

:::note
The prices on this page apply to standard Dragonfly Cloud data stores. Pricing for
[Bring Your Own Cloud (BYOC)](../byoc/byoc.md) is different. To get a quote, contact
[support@dragonflydb.io](mailto:support@dragonflydb.io) or [request a demo](https://www.dragonflydb.io/request-demo).
:::

## Price Summary

| Component | How it is charged |
|-----------|-------------------|
| Active data stores | Per GB of provisioned memory per month, prorated hourly. Depends on the compute performance tier (**Standard**, **Enhanced**, **Extreme**), cloud provider, and region. For example, 1 GB on the **Enhanced** tier in AWS `us-east-1` is **$11.0 per month**. |
| Data transfer | Public data transfer rates set by the cloud vendor. |

## Active Data Stores

Data stores incur charges for **every prorated hour they are active**.
The cost is determined by:

- **Provisioned Memory Size**[^1]
- **Compute Performance Tier**[^2]
- **Cloud Provider & Region**

Additional notes about active data store costs:

- Updating a data store configuration only affects its cost once the update is complete
  and the new configuration is active.
- Deleted data stores do not incur any charges.

### Active Data Store Cost Calculation

You can use the following tools to get **an accurate estimate** of your active data store costs:

- Use the [pricing calculator](https://www.dragonflydb.io/pricing#calculator) to estimate the cost of a data store
  based on its memory size, cloud provider, and region.
- In [Dragonfly Cloud](https://dragonflydb.cloud/), the data store cost (excluding data transfer cost)
  is displayed every time you create or update a data store.

### Active Data Store Cost Example

To illustrate with an example, let's consider a Dragonfly Cloud data store that is:

- Configured with **12.5 GB** of provisioned memory on the **Enhanced** compute tier.
- Configured with **2 zones**, one primary and one replica.
- Located in the **AWS us-east-1** region.
- Active for **2 days, 1 hour, and 10 minutes**.

The cost of this data store can be calculated as follows:

- Cost for 1 GB of the **Enhanced** compute tier data store in the AWS us-east-1 region = **$11.0 per month**.
- Total hours used: 2 days x 24 hours per day + 1 hour + 10 minutes (rounded up to 1 hour) = **50 hours**.
- Total hours in a month: 365 days / 12 months x 24 hours per day = **730 hours per month**.
- Total cost: **$11 x 12.5 GB x 2 zones x 50 hours / 730 hours per month = $18.84**

## Data Transfer

- Data transfer fees are costs imposed by cloud providers for moving data across various destinations,
  including between clouds, the public internet, different cloud regions, and even between availability zones
  within the same region.
- Dragonfly Cloud applies public data transfer fee rates set by cloud vendors for data store traffic.
  For detailed and specific pricing, please refer to the [AWS](https://aws.amazon.com/ec2/pricing/on-demand/), [GCP](https://cloud.google.com/vpc/network-pricing) and [Azure](https://azure.microsoft.com/en-us/pricing/details/bandwidth/) pricing pages.
- **To reduce data transfer expenses, using [data stores with a private network](../datastores.md#private-endpoint) is
  recommended**.
- Additionally, data stores with high availability configuration may incur charges for cross-availability-zone traffic
  within the cloud provider's network.


[^1]: The total memory provisioned to the data store, including all primary and replica Dragonfly server instances.

[^2]: The compute performance tier determines the CPU-to-memory ratio for the data store. Currently, Dragonfly Cloud
offers **Standard**, **Enhanced**, and **Extreme** performance tiers.
Read more [here](../datastores.md#creating-a-data-store).
