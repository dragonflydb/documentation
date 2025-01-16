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

## Azure (Private Beta)

Currently, Azure peering connections are in private beta. If you face any issues, please contact us.

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
