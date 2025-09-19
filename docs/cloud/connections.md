---
sidebar_position: 5
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Peering Connections
<CloudBadge/>
<PageTitle title="Peering Connections | Dragonfly Cloud" />

## Overview



**Peering connections** are used to connect a Dragonfly Cloud private network with a VPC in your
cloud provider account to establish communication between the two networks over private IP space.
Private IP space communication is **more secure, more performant,
and reduces data transfer costs** incurred by cloud providers.

Once you have a private network created, as described in the [networks](./networks) section,
you can create a peering connection by clicking the three-dot
menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>)
on the right side of the network and then clicking the **+Connect** button,
or simply by clicking the **+Add Connection** button under the network itself.

Continue to the next sections for instructions on how to create a peering connection with your cloud provider.

*Tip:* For connecting to a private network from a local machine, see [Connect with VPN](./connect/vpn).

---

## Amazon Web Services (AWS)

Follow the steps below to create a peering connection within the Dragonfly Cloud console,
and then accept the peering connection in your AWS account console:

- In the **Networks** tab of the Dragonfly Cloud console, click the **+Add Connection** button,
  and a dialog will appear.
- Specify a **Name**, the **Acceptor Region**, the **Acceptor Account ID** (also called owner ID in AWS),
  and the **Acceptor VPC ID** of your AWS VPC from where you want to connect, and click **Create**.
- The connection will be created in the **Inactive** status.
- Next, you should accept the peering connection in your AWS account console (**VPC > Peering Connections**).
- Create a route in your AWS VPC's route table (**Route Table > Edit Routes > Add Route**):
  - Set the **Destination** to the CIDR of the Dragonfly Cloud private network (i.e., `192.168.0.0/16`).
  - Set the **Target** to the AWS peering connection ID (i.e., `pcx-0f727XXXXXXXXXXXX`).
- Modify your relevant security groups to allow traffic from the Dragonfly Cloud private network CIDR.
- Observe the connection becoming **Active** after a few moments in the Dragonfly Cloud console.

You can read more about AWS peering
connections [here](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html).
If you haven't done so already, create a data store with a private endpoint and start building your applications with
it. Read more about creating a data store with a private endpoint [here](./datastores#private-endpoint).

---

## Google Cloud Platform (GCP)

Follow the steps below to create a peering connection within the Dragonfly Cloud console,
and then accept the peering connection in your GCP account console:

- In the **Networks** tab of the Dragonfly Cloud console, click the **+Add Connection** button
  and a dialog will appear.
- Specify a **Name**, the **Acceptor Account ID** (the GCP project ID),
  and the **Acceptor VPC ID** of your GCP VPC from where you want to connect, and click **Create**.
- The connection will be created in the **Inactive** status.
- Next, you should accept the peering connection using your GCP account.
- Follow the Google Cloud guide [here](https://cloud.google.com/sdk/gcloud/reference/compute/networks/peerings/create),
  specify `--peer-network` and `--peer-project` with the **VPC ID** and **Account ID** values from the Dragonfly Cloud
  private network you wish to connect.
- Observe the connection becoming **Active** after a few moments in the Dragonfly Cloud console.
- Don't forget to modify your firewall to allow traffic from the Dragonfly Cloud private network CIDR.

---

## Microsoft Azure

In Azure, For two Vnets be peered, both sides need to have access to each other's Vnet. For this, Peering permissions are given to the Dragonfly Cloud's Azure AD application on your Vnet. On the client side, A new Azure AD application is created and given permissions to the Dragonfly Cloud's Vnet. You can learn more about Azure Vnet peering [here](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview).

Make sure to have created a private network in Dragonfly Cloud before proceeding.

### 1. Set Required Environment Variables

Before starting, set these variables in your shell:

```bash
# Required Azure Information
user_subscription_id=""      # Your Azure subscription ID
user_resource_group=""      # Your Azure resource group name
user_vnet_name=""          # Your Azure VNet name
azure_region=""            # Your Azure region (e.g., centralus)
dfcloud_account_id=""        # Account ID under the user created Dragonfly Cloud network
dfcloud_vpc_id=""            # VPC ID under the user created Dragonfly Cloud network

# dfcloud_account_id + "/providers/Microsoft.Network/virtualNetworks/" + dfcloud_vpc_id
dfcloud_vnet_id="$dfcloud_account_id/providers/Microsoft.Network/virtualNetworks/$dfcloud_vpc_id"

# Dragonfly Cloud Related
dfcloud_tenant_id="3f7cbd78-1650-4b7d-b28f-8ee05eac10a4"  # Fixed value

# Clear any existing Azure login
az account clear
```

### 2. Create Azure AD Application and Service Principal

Create an Azure AD application for peering authentication:

```bash
# Login with your client account
az login

# Create the application
user_app_id=$(az ad app create --display-name client-app --sign-in-audience AzureADMultipleOrgs --key-type Password --query appId -o tsv)

# Create service principal
user_sp_id=$(az ad sp create --id $user_app_id --query id -o tsv)
```

### 3. Get Additional Network Details

Collect the remaining network information:

```bash
# Get tenant ID and VNet ID
user_tenant_id=$(az account show --subscription $user_subscription_id --query tenantId -o tsv)
user_vnet_id=$(az network vnet show --subscription $user_subscription_id --name $user_vnet_name --resource-group $user_resource_group --query id -o tsv)
```

### 4. Assign Required Roles

Set up the necessary permissions for both your application and Dragonfly Cloud:

```bash
# Assign Network Contributor role to your service principal
az role assignment create --subscription $user_subscription_id --role "Network Contributor" --assignee-object-id $user_sp_id --scope $user_vnet_id

# Create service principal for Dragonfly Cloud
dfcloud_sp_id=$(az ad sp create --id ac30c41f-1eab-4f45-9024-70decee5559d --query id -o tsv)

# Create custom role for Dragonfly Cloud
dfcloud_role_id=$(az role definition create --subscription $user_subscription_id --role-definition '{
  "Name": "dfcloud-peering-role",
  "Description": "Allows creating a peering to vnets in scope (but not from)",
  "Actions": ["Microsoft.Network/virtualNetworks/peer/action"],
  "AssignableScopes": ["/subscriptions/'$user_subscription_id'"]
}' --query name -o tsv)

# Assign the custom role to Dragonfly Cloud
az role assignment create --subscription $user_subscription_id --role $dfcloud_role_id --assignee-object-id $dfcloud_sp_id --scope $user_vnet_id
```

### 5. Create Connection in Dragonfly Cloud Console

In the Dragonfly Cloud console, create a new connection with these details:

- **Acceptor Account ID**: Your Azure subscription ID (`$user_subscription_id`)
- **Acceptor VPC ID**: Your VNet name (`$user_vnet_name`)
- **Acceptor Region**: Your Azure region (`$azure_region`)
- **App ID**: Your Azure AD application ID (`$user_app_id`)
- **Resource Group**: Your resource group name (`$user_resource_group`)
- **Tenant ID**: Your Azure tenant ID (`$user_tenant_id`)

The connection will be created in an **Inactive** state. If the connection fails, please check if all the details are correct.

With this step, Dragonfly Cloud has created a peering connection on its side using the Azure AD application credentials to which you have assigned the necessary permissions.

### 6. Create Azure Peering Connection

After the connection is created in Dragonfly Cloud, establish the peering from your client side using the application credentials which now
has access to both the Dragonfly Cloud Azure VNet and your Azure VNet.

```bash
# Reset and get new credentials
az ad app credential reset --id $user_app_id

# Clear existing login and authenticate
az account clear
az login --service-principal -u $user_app_id -p <password> --tenant $user_tenant_id
az login --service-principal -u $user_app_id -p <password> --tenant $dfcloud_tenant_id

# Create the peering connection
az network vnet peering create \
    --name $user_vnet_name-dfcloud-peering \
    --resource-group $user_resource_group \
    --vnet-name $user_vnet_name \
    --remote-vnet $dfcloud_vnet_id \
    --subscription $user_subscription_id \
    --allow-vnet-access
```

The connection will become **Active** after peering is established.

With Azure, By default the `AllowVnetInbound` and `AllowVnetOutbound` rules allow traffic between the two peered networks. If you don't have this rule, please make sure to
add the required firewall rule to allow `6379` port traffic between the two networks.


If you haven't done so already, create a data store with a private endpoint and start building your applications with
it. Read more about creating a data store with a private endpoint [here](./datastores#private-endpoint).
