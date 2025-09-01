---
sidebar_position: 1
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# AWS Client VPN

<CloudBadge/>
<br /><br />

<PageTitle title="Connecting with AWS Client VPN | Dragonfly Cloud" />

[AWS Client VPN](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html) is a managed client-based VPN service that enables you to securely access your AWS resources. With Client VPN, you can access your resources from any location using an OpenVPN-based VPN client.
To connect to a private endpoint datastore from your local machine, you need to create a Client VPN endpoint in your VPC that is peer connected to the Dragonfly Cloud private network where your private endpoint datastore is deployed.

Connecting via AWS Client VPN involves the following steps:

1. Create server and client certificates.
2. Import the server certificate to AWS Certificate Manager.
3. Locate or create a security group for the Client VPN endpoint.
4. Create and configure a Client VPN endpoint.
5. Download the Client VPN endpoint configuration file and update it with the client certificate.
6. Connect to the Client VPN endpoint using the OpenVPN client.

## Create server and client certificates

We will use the `easy-rsa` tool to create server and client certificates.

Execute the following commands to create the server and client certificates, chose default values when prompted:

```bash
# Clone the easy-rsa repository
git clone https://github.com/OpenVPN/easy-rsa.git

# generate the server and client certificates
cd easy-rsa/easyrsa3
./easyrsa init-pki
./easyrsa build-ca nopass

# we use server as the common name for the server certificate, but you can use any name
./easyrsa --san=DNS:server build-server-full server nopass

# we use client1.domain.tld as the common name for the client certificate, but you can use any name
./easyrsa build-client-full client1.domain.tld nopass

# for convinience, copy the certificates to the current directory
cp pki/ca.crt pki/issued/server.crt pki/private/server.key pki/issued/client1.domain.tld.crt pki/private/client1.domain.tld.key .
```

## Import the certificates to AWS Certificate Manager

Navigate to _ASW Certificate Manager_ (ACM) in the AWS console.

**_Note:_** Make sure you are in the same the region of your VPC which is peer connected to the Dragonfly Cloud private network, which is the region where you will also create the Client VPN endpoint.

Click _Import certificate_ to import the server certificate.

`cat server.crt` and copy the output to the _Certificate body_ field.
`cat server.key` and copy the output to the _Certificate private_ key field.
`cat ca.crt` and copy the output to the _Certificate chain_ field.

Click _Import certificate_

Repeat the same steps to import the client certificate, with the contents of `cat client1.domain.tld.crt`, `cat client1.domain.tld.key` and the same `cat ca.crt file`.

## Locate or create a security group

We'll need to attach to the Client VPN endpoint a security group that allows inbound traffic on port 443.

```bash
aws ec2 create-security-group --group-name client-vpn-sg --description "Client VPN security group" --vpc-id vpc-xxxxxxxx
```

Replace `vpc-xxxxxxxx` with the ID of the VPC where you want to create the security group.

Add a rule to allow inbound traffic on port 443 from anywhere:

```bash
aws ec2 authorize-security-group-ingress --group-id sg-xxxxxxxx --protocol tcp --port 443 --cidr 0.0.0.0/0
```

Replace `sg-xxxxxxxx` with the ID of the security group you created.

## Create and configure a Client VPN endpoint

Navigate to _Client VPN Endpoints_ in the AWS console.

Click _Create Client VPN endpoint_.

Fill in the following fields, leaving the rest as default:

- **_Name_** - A name for the Client VPN endpoint.
- **_Description_** - A description for the Client VPN endpoint.
- **_Client IPv4 CIDR_** - The CIDR block for the Client VPN endpoint.  
  This should be a private IP range that does not overlap with the CIDR blocks of the your VPC or the Dragonfly Cloud private network.  
  E.g. if your VPC CIDR block is 172.31.0.0/16 and the Dragonfly Cloud private network CIDR block is 10.5.0.0/16, you can use 172.32.0.0/16.
- **_Server certificate ARN_** - Select the ARN of the server certificate you imported to ACM.
- Under _Authentication options_ - select _Mutual authentication_.
  - **_Client certificate ARNs_** dropdown will appear, select the ARN of the client certificate you imported to ACM.
- **_DNS server 1 IP address_** - The IP address of the DNS server in your VPC.  
  This is the 3rd IP address in the CIDR block of your VPC. E.g. if your VPC CIDR block is 172.31.0.0/16, the DNS server IP address is 172.31.0.2/16.
- **_Enable split-tunnel_** - Optional but recommended, [learn more](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/split-tunnel-vpn.html).
- **_DNS server 2 IP address_** - Enter 8.8.8.8 (Google's public DNS server).
- **_VPC ID_** - Select the VPC where you want to create the Client VPN endpoint. This should be the VPC that is peer connected to the Dragonfly Cloud private network.
  - **_Security group_** dropdown will appear - Select the security group you created or located for the Client VPN endpoint.

Finally, click _Create Client VPN endpoint_.

### Configure the Client VPN endpoint

The Client VPN endpoint will be created in a _pending association_ state.
Select the Client VPN endpoint and click _Associate target network_.

Select the \*Target network associations tab, if it is not already selected.

For **_VPC_** select the VPC that is peer connected to the Dragonfly Cloud private network.
For **_Subnet_** you can select any subnet in the VPC.

click _Associate target network_.

Next, select the Security group tab and verify that the security group you created or located previously is attached to the Client VPN endpoint.

Next, select the _Authorization rules_ tab and click _Add authorization rule_.
Enter _Destination network to enable access_ as the CIDR block of the VPC that is peer connected to the Dragonfly Cloud private network.
Repeat for the CIDR block of the Dragonfly Cloud private network.
You should have two authorization rules, one for each VPC.

Next, select the _Route table_ tab and click _Create route_.
You should see an already existing route with description _default route_.
Click _Create route_.
For _Route destination_ enter the CIDR block of the Dragonfly Cloud private network.
For _Subnet ID for target network association_ select the same subnet you selected when associating the target network.
This will route traffic to the Dragonfly Cloud private network through the Client VPN endpoint.

By now, the Client VPN endpoint should be in the _available_ state, otherwise wait for a few more minutes.

## Download the Client VPN endpoint configuration file and update it with the client certificate

Select the Client VPN endpoint and click _Download client configuration_.

Open the downloaded file for edit.
Under the existing `ca` block, add the following blocks:

```bash
<cert>
#... contents of your client1.domain.tld.crt file
</cert>

<key>
#... contents of your client1.domain.tld.key file
</key>
```

Save the file.

## Connect to the Client VPN endpoint using the OpenVPN client

Install the AWS VPN client from [this .deb packed](https://d20adtppz83p9s.cloudfront.net/GTK/latest/awsvpnclient_amd64.deb).
Or see other installation options [here](hhttps://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-connect-linux-install.html).

Launch the OpenVPN client.

From the file menu select _manage profiles_ and click _Add profile_.
Enter a _display name_ for the profile and select the _VPN Configuration File_ you downloaded and updated previously.

After adding the profile, click _Connect_ next to the profile you have just added.
Once the profile is connected, you should be able to access the private endpoint datastore from your local machine.
