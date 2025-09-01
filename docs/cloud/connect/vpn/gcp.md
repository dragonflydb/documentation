---
title: Google Cloud VPN
description: Connect to your private Dragonfly Cloud instance using Google Cloud VPN
sidebar_position: 2
slug: /cloud/connect/vpn/gcp
---

import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Google Cloud VPN

<CloudBadge/>
<br /><br />

This guide shows how to connect to your private Dragonfly Cloud instance using Google Cloud VPN.

## Prerequisites

- A Google Cloud account with appropriate permissions
- A Dragonfly Cloud instance deployed in Google Cloud with a private endpoint
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed on your machine
- OpenVPN client software installed on your local machine

## Setting Up Cloud VPN

### Step 1: Create a VPN Gateway

1. Navigate to the [VPN page](https://console.cloud.google.com/networking/vpn/list) in the Google Cloud Console
2. Click on "Create VPN Connection" and select "HA VPN"
3. Enter a name for your VPN gateway
4. Select the same region as your Dragonfly Cloud instance
5. Click "Create"

### Step 2: Create a Cloud Router

1. Click "Create Cloud Router"
2. Enter a name for your router
3. Select the same region as your VPN gateway
4. Choose a Google ASN (Autonomous System Number)
5. Click "Create"

### Step 3: Create External VPN Gateway

1. Navigate to "External VPN gateways" in the left menu
2. Click "Create external VPN gateway"
3. Enter a name and the appropriate interface IP addresses
4. Click "Create"

### Step 4: Create VPN Tunnels

1. Return to the HA VPN gateways page
2. Click on your newly created gateway
3. Click "Create VPN tunnel"
4. Configure the tunnel settings to match your network requirements
5. Create a second tunnel for high availability
6. Configure BGP sessions for each tunnel

### Step 5: Configure Client VPN

1. Download the OpenVPN configuration file from the Google Cloud Console
2. Import the configuration into your OpenVPN client
3. Connect to your VPN using your credentials

## Connecting to Dragonfly Cloud

Once your VPN connection is established:

1. Use your standard Dragonfly client with the private endpoint address
2. Your connection is now securely tunneled through the VPN

```python
import dragonfly

# Connect to your private Dragonfly Cloud instance through VPN
client = dragonfly.connect(
    host='your-private-endpoint.internal',
    port=6379
)

# Now you can interact with your Dragonfly instance
client.set('key', 'value')
result = client.get('key')
print(result)  # Outputs: 'value'
```

## Troubleshooting

If you encounter connectivity issues:

1. Verify your VPN connection is active
2. Check that your VPN routes include the subnet of your Dragonfly instance
3. Ensure your firewall rules allow traffic to the Dragonfly port
4. Confirm your Dragonfly instance's network policy allows your VPN subnet

For additional assistance, please contact Dragonfly Cloud support.
