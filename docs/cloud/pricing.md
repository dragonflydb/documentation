---
sidebar_position: 7
---

# Pricing
Dragonfly Cloud applies a transparent usage based pricing with the following components
1. Active data stores
2. Data transfer
3. Backup storage

You can track your usage and cost under the *Account > Usage* tab.  
The usage and cost information is updated every few hours, data transfer and storage costs might lag for 24 hours.

Read further for more details on each component.


## Active Data Stores

Data stores incur charges for every hour they are active.
Data store cost is based on the amount of provisioned memory,  performance tier, cloud provider and region. 

For example:
Consider a 2 zones, 12.5 BG enhanced performance tier data store active for 2 days 1 hour and 10 minutes.  
1 GB of enhanced performance tier data store in AWS us-east1 costs $11.0 per month.  
Total hours used is 50 hours.  
Datastore usage cost is *$11 x 12.5 GB x 2 Zones x 50 Hours  / (365 / 12 x 24) = $18.84*

Updating your data store configuration only affects its cost once the update is complete and the new configuration is active.

Deleted data stores do not incur any charges.

## Data Transfer 

Data transfer fees are costs imposed by cloud providers for transferring data across various destinations: between clouds, the public internet, different cloud regions, and even between availability zones within the same region.  

Dragonfly Cloud applies public data transfer fee rates set by cloud vendors for data store traffic. For detailed and specific pricing, please refer to the [AWS](https://aws.amazon.com/ec2/pricing/on-demand/) and [GCP](https://cloud.google.com/vpc/network-pricing) pages.  

***To reduce data transfer expenses, using [data stores with private endpoints](./datastores.md#private-endpoint) is recommended***.  
Additionally, high-availability data stores may incur charges for cross-availability zone traffic within the cloud provider's network.

## Backup Storage

Backup storage costs $0.1 per GB per month, prorated hourly.
