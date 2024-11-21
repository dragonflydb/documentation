---
sidebar_position: 4
---

# Peering Connections

*Peering connections* are used  to connect a Dragonfly Cloud private network with a VPC in your cloud account to establish communication between the two networks over private IP space.

Private IP space communication is more secure, performant and reduces data transfer costs incurred by cloud providers.

Once you create a *private network* as described in [Networks](./networks), click the network three dots menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) and click *+ Connect*

Continue to [AWS](#aws) or [GCP](#gcp) based on your cloud provider.


## AWS
Specify the *region*, *CIDR*, *account ID* (also called owner ID in AWS) and *VPC ID* of your AWS VPC from where you want to connect and click *Create*.

The connection will be created in an **Inactive** state.

Following, you should accept the peering connection in your AWS account console (VPC > Peering Connections). 
Create a route in your AWS VPC, set the destination to the CIDR of the Dragonfly Cloud private network, set the target to the AWS peering connection ID.
More information about AWS peering connection [here](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html).

Modify your relevant security groups to allow traffic from the Dragonfly cloud Private Network CIDR.

At this point you should see the connection in state **Active** in the Dragonfly Cloud console.

If you haven’t done so already, create a data store with a private endpoint. See [Data Stores](./datastores#private-endpoint) for more information.


##  GCP
Specify the *CIDR*, GCP *project ID* and *VPC ID* of your GCP VPC from where you want to connect and click Create.

The connection will be created in an **Inactive** state. Follow the Google Cloud guide <a href="https://cloud.google.com/sdk/gcloud/reference/compute/networks/peerings/create">here</a> , specify `--peer-network` and `--peer-project` with the VPC ID and account ID values from the Dragonfly Cloud private network you wish to connect. Observe the connection becomes **Active** after a few moments.      

Don't forget to modify your firewall to allow traffic from the Dragonfly cloud Private Network CIDR.

If you haven’t done so already, create a data store with a private endpoint.
