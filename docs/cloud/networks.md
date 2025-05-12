---
sidebar_position: 3
---

import PageTitle from '@site/src/components/PageTitle';

# Networks

<PageTitle title="Private Networks | Dragonfly Cloud" />

## Overview

Dragonfly Cloud allows you to create private **networks** for your data stores.
Like data stores, networks are important resources you can manage in your Dragonfly Cloud account.
After creating a private network, you can:

- Create a **VPC peering connection** to connect the Dragonfly Cloud private network with a [VPC](https://en.wikipedia.org/wiki/Virtual_private_cloud) in your cloud provider account
  to establish communication between the two networks over private IP space. Read more on [peering connections](./connections.md).
- Create a data store in the private network with a **private endpoint**. Read more on [data store security](./datastores#security).

**Note: By default, each Dragonfly Cloud account has a quota of two private networks.**
If you need more private networks, please contact support.

## Creating a Private Network

A private endpoint data store in a private network provides better security and performance and reduces data transfer costs.
To create a private network:

- Navigate to the **Networks** tab and click the [+Network](https://dragonflydb.cloud/networks/new) button.
- Specify a **Name**, a **Cloud Provider**, and a **Cloud Region** for your network.
- Specify the **CIDR** block (IP range) for your network.
- The CIDR of the Dragonfly Cloud network must not overlap with any CIDR of your application VPC from where the requests or commands will be sent to the data store.
- For example, the following [CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation) pairs are overlapping:
  - **192.168**.0.0/**16**, **192.168**.0.0/**16**
  - **192.168**.0.0/**16**, **192.168.1**.0/**24**
- While the following CIDR pairs are not overlapping:
  - **192.168**.0.0/**16**, **172.16**.0.0/**16**
  - **192.168**.0.0/**16**, **172.16**.1.0/**24**
- Once done, click **Create** and observe the network status become **Active**.

See [peering connections](./connections.md) to connect the Dragonfly Cloud network to a VPC in your
cloud provider account in order to establish communication between the two networks.

For connecting to private network from a local machine, see [Connect with VPN](./connect/vpn/).
