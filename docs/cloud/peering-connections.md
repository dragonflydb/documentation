---
sidebar_position: 4
---

# Peering Connections

## Overview

**Peering connections** are used to connect a Dragonfly Cloud private network with a VPC in your
cloud provider account to establish communication between the two networks over private IP space.
Private IP space communication is **more secure, more performant,
and reduces data transfer costs** incurred by cloud providers.

Once you have a private network created, as described in the [networks](./networks) section,
you can create a peering connection by clicking the three dots
menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>)
on the right side of the network and then clicking the **+ Connect** button,
or simply by clicking the **+ Add Connect** button under the network itself.

Continue to the next sections for instructions on how to create a peering connection with your cloud provider.

## AWS

Follow the steps below to create a peering connection within the Dragonfly Cloud console,
and then accept the peering connection in your AWS account console:

- In the Networks tab of the Dragonfly Cloud console, click the **+ Add Connect** button, and a dialog will appear.
- Specify a **Name**, the **Acceptor Region**, the **Acceptor Account ID** (also called owner ID in AWS),
  and the **Acceptor VPC ID** of your AWS VPC from where you want to connect, and click **Create**.
- The connection will be created in the **Inactive** status.
- Next, you should accept the peering connection in your AWS account console (**VPC > Peering Connections**).
- Create a route in your AWS VPC, set the destination to the CIDR of the Dragonfly Cloud private network,
  and set the target to the AWS peering connection ID.
- You can read more about AWS peering
  connections [here](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html).
- Modify your relevant security groups to allow traffic from the Dragonfly Cloud private network CIDR.
- Observe the connection becoming **Active** after a few moments in the Dragonfly Cloud console.

If you haven't done so already, create a data store with a private endpoint and start building your applications with
it. Read more about creating a data store with a private endpoint [here](./data-stores#private-endpoint).

## GCP

Follow the steps below to create a peering connection within the Dragonfly Cloud console,
and then accept the peering connection in your GCP account console:

- In the Networks tab of the Dragonfly Cloud console, click the **+ Add Connect** button, and a dialog will appear.
- Specify a **Name**, the **Acceptor Account ID** (the GCP project ID),
  and the **Acceptor VPC ID** of your GCP VPC from where you want to connect, and click **Create**.
- The connection will be created in the **Inactive** status.
- Next, you should accept the peering connection using your GCP account.
- Follow the Google Cloud guide [here](https://cloud.google.com/sdk/gcloud/reference/compute/networks/peerings/create),
  specify `--peer-network` and `--peer-project` with the **VPC ID** and **Account ID** values from the Dragonfly Cloud
  private network you wish to connect.
- Observe the connection becoming **Active** after a few moments in the Dragonfly Cloud console.
- Don't forget to modify your firewall to allow traffic from the Dragonfly Cloud private network CIDR.

If you haven't done so already, create a data store with a private endpoint and start building your applications with
it. Read more about creating a data store with a private endpoint [here](./data-stores#private-endpoint).
