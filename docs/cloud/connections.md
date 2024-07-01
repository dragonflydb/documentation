---
sidebar_position: 4
---

# Peering Connections

*Peering connections* are used  to connect a Dragonfly Cloud private network with a VPC in your cloud account to establish communication between the two networks over private IP space.

Private IP space communication is more secure, performant and reduces data transfer costs incurred by cloud providers.

Once you creat a *private network* as described in [Networks](./networks), click the network three dots menu and click **+ Connect**

Continue to [AWS](#aws) or [GCP](#gcp) based on your cloud provider.


## AWS
Specify the *region*, *CIDR*, *account ID* (also called owner ID in AWS) and *VPC ID* of your AWS VPC from where you want to connect and click *Create*.

The connection will be created in an inactive state.

Following, you should accept the peering connection in your AWS account console (VPC > Peering Connections). 
Create a route in your AWS VPC, set the destination to the CIDR of the Dragonfly Cloud private network, set the target to the AWS peering connection ID.
More information about AWS peering connection [here](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html).

At this point you should see the connection in state *Active* in the Dragonfly Cloud console.

If you haven’t done so already, create a data store with a private endpoint. See [Data Stores](./datastores#private-endpoint) for more information.


##  GCP
Specify the *CIDR*, GCP *project ID* and *VPC ID* of your GCP VPC from where you want to connect and click Create.

The connection will be created in an inactive state. Follow the Google Cloud guide <a href="https://cloud.google.com/sdk/gcloud/reference/compute/networks/peerings/create">here</a> , specify `--peer-network` and `--peer-project` with the account ID and VPC ID values from the Dragonfly Cloud private network you wish to connect. Observe the connection becomes active after a few moments.      

If you haven’t done so already, create a data store with a private endpoint.
