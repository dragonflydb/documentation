---
description: Learn how to privately connect to a Dragonfly Cloud data store from your Azure virtual network using Azure Private Link.
sidebar_position: 5.5
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Private Links

<CloudBadge/>
<PageTitle title="Private Links | Dragonfly Cloud" />

:::note
Private Links are currently supported on **Microsoft Azure** only.
This page describes how to use [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview) with Dragonfly Cloud.
:::

[Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview) lets you reach a
Dragonfly Cloud data store from your Azure virtual network (VNet) through a **Private Endpoint** in your own subscription.
Traffic stays on the Microsoft backbone network and never traverses the public internet.

Connecting via Azure Private Link involves the following steps:

1. Create a private network in Azure.
2. Add a Private Link to the network in the Dragonfly Cloud console.
3. Create a Private Endpoint in your Azure subscription.
4. Create a data store with the Private Endpoint IP address.
5. Connect to the data store.

## Prerequisites

- A Dragonfly Cloud account with permission to create networks, Private Links, and data stores.
- One or more Azure subscriptions from which you will create the Private Endpoint.
  You will need their subscription IDs (for example, `00000000-0000-0000-0000-000000000000`).

## Limitations

- Azure Private Link is available for networks and data stores in the **Microsoft Azure** cloud provider only.
- A network can have **at most one** Private Link.
- Private Link is **not supported for cluster mode** data stores.
- A data store must be in a private network to use Private Link.

## Step 1: Create a Private Network

Create a private network in the Azure region where you want to deploy your data store.
See [Networks](./networks.md#creating-a-private-network) for details.
Wait until the network status becomes **Active**.

## Step 2: Add a Private Link to the Network

1. Navigate to the **Networks** tab.
2. Click the **+Private Link** button under the network, or open the three-dot menu on the right side of the network
   and select **Add Private Link**. This option is only available for **Active** Azure networks.
3. In the **Add Private Link** dialog, enter the **Azure Subscription IDs** that are allowed to connect.
   Click **Add Subscription ID** to add more than one.
   Each ID must be a valid UUID, and duplicates are rejected.
4. Click **Create**.

Dragonfly Cloud provisions a Private Link Service for the network. Its **Status** goes from `pending` to `active`
once it is ready to accept a Private Endpoint connection. If provisioning fails, the status shows `failed`;
hover over the info icon next to it to see the reason.

Once active, the Private Link row under the network shows the following details, each with a copy button:

| Field                | Description                                                                          |
| -------------------- | ------------------------------------------------------------------------------------ |
| **ID**               | The Dragonfly Cloud identifier of the Private Link.                                  |
| **Alias**            | The Private Link Service alias, used to create the Private Endpoint in Azure.        |
| **Resource ID**      | The Azure resource ID of the Private Link Service.                                   |
| **Subscription IDs** | The Azure subscriptions whose Private Endpoint connections are approved automatically. |

## Step 3: Create a Private Endpoint in Azure

In the [Azure portal](https://portal.azure.com), create a Private Endpoint in the VNet from which your applications connect:

1. Search for **Private endpoints** and click **Create**.
2. Select one of the subscriptions you listed in Step 2, and choose the resource group and region.
3. On the **Resource** tab, set **Connection method** to **Connect to an Azure resource by resource ID or alias**.
4. Paste the **Alias** (or **Resource ID**) copied from the Private Link row in Dragonfly Cloud.
5. On the **Virtual Network** tab, select the VNet and subnet, and assign an IP address to the endpoint.
6. Complete the wizard and create the endpoint.

Because the Private Link is configured with your subscription IDs, the connection is **approved automatically**,
with no action required from Dragonfly Cloud.

After the endpoint is created, note its **private IP address** (shown on the Private Endpoint's network interface).
You will need it in the next step.

:::note
The Private Endpoint must be created in a subscription listed in the Private Link configuration.
Connections from other subscriptions are not approved.
:::

## Step 4: Create a Data Store with the Private Link IP

1. Navigate to the **Data Stores** tab and click **+Data Store**.
2. Select **Microsoft Azure** as the **Cloud Provider** and the same region as your network.
3. In the **Security** section, set **Endpoint** to the private network created in Step 1.
4. Enter the Private Endpoint's IP address in the **Private Link IP** field. It must be a valid IPv4 address.
   This field is only shown for Azure data stores in a private network that are not in cluster mode.
5. Complete the rest of the form and click **Create**.

The data store is then reachable through the Private Link. You can also set or change **Private Link IP**
for an existing data store from its edit view. Changing the data store's network clears the field.

## Step 5: Connect to the Data Store

Once a Private Link IP is configured, Dragonfly Cloud assigns the data store a dedicated **Private Link port** on the
Private Link's load balancer and points the data store's DNS name to your **Private Endpoint IP**.
You can therefore connect with the data store's hostname, but you **must** use the Private Link port
instead of the default data store port:

```shell
redis-cli -u rediss://default:<password>@<datastore-hostname>:<private-link-port>
```

The scheme is `rediss://` when TLS is enabled on the data store, and `redis://` otherwise.
The Private Link port is shown in the data store's connection details.
Connect from a machine inside the VNet (or a network peered with it) where the Private Endpoint is reachable.

:::note
The Private Link port is assigned shortly after the Private Link IP is set, and the DNS name is switched to the
Private Endpoint IP at the same time. Until then, the data store's hostname resolves to its regular private address.
:::

## Deleting a Private Link

Open the three-dot menu on the Private Link row and select **Delete**. This is available when the Private Link
status is `active` or `failed`, and requires permission to delete Private Links.

:::warning
Deleting a Private Link deletes the Private Link Service. Private Endpoints connected to it stop working,
and data stores using it are no longer reachable through it.
:::

## Troubleshooting

| Symptom                                           | What to check                                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Add Private Link** is disabled                  | The network must be an **Active** Azure network without an existing Private Link, and you need permission to create Private Links. |
| "Invalid or duplicate subscription ID" error      | Each subscription ID must be a valid UUID and listed once.                                             |
| Private Link status is `failed`                   | Hover over the info icon next to the status for details, delete the Private Link, and create it again. |
| Cannot connect from the VNet                      | Verify the Private Endpoint connection is approved, the **Private Link IP** matches the endpoint IP, the data store's hostname resolves to that IP, and you are using the Private Link port rather than the default port. |
