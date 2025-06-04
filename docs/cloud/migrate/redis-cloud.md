---
title: Redis Cloud
description: The following guide will help you migrate from Redis Cloud to Dragonfly Cloud
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import { ConfigDisplay } from './_migration_options.mdx';
import BrowserOnly from '@docusaurus/BrowserOnly';

# Redis Cloud Migration

In this guide, we will walk you through the steps to migrate from Redis Cloud to Dragonfly Cloud.

<BrowserOnly>
{() => (
  <ConfigDisplay
    isCluster={new URLSearchParams(window.location.search).get('cluster') === 'true'}
    isSync={false}
  />
)}
</BrowserOnly>

:::tip Need Help?
If you have any questions or need assistance with your migration, our team is here to help! Join our [Discord community](https://discord.gg/HsPjXGVH85) for real-time support.
:::

## Prerequisites

Before starting the migration, ensure you have:

1. Access to your Redis Cloud endpoint and credentials
2. A Dragonfly Cloud Network peered with your application's VPC (APP_VPC_ID). Follow the [instructions here](/docs/cloud/connections.md) to peer your VPC with Dragonfly Cloud
3. A Dragonfly Cloud Datastore in the private network. Follow the [instructions here](/docs/cloud/datastores.md) to create a datastore
4. AWS CLI configured with appropriate permissions

## Migration Steps

### 1. Launch EC2 Instance in Application VPC

1. Set up environment variables:

```bash
# Set the Application VPC details
APP_VPC_ID=<your-application-vpc-id>  # VPC where your application resides and Dragonfly Cloud is peered
APP_SUBNET_ID=<your-application-subnet-id>

# Set Redis Cloud details
REDIS_CLOUD_URL=<your-redis-cloud-url>
REDIS_CLOUD_PORT=<your-redis-cloud-port>
REDIS_CLOUD_PASSWORD=<your-redis-cloud-password>

# Set the Dragonfly Cloud Datastore details
DRAGONFLY_CLOUD_URL=<your-dragonfly-cloud-url>
# not needed if its a private datastore (and password is not set)
DRAGONFLY_CLOUD_PASSWORD=<your-dragonfly-cloud-password>
```

2. Create security group for migration instance:

```bash
# Create security group
REDISSHAKE_SG_ID=$(aws ec2 create-security-group \
  --group-name migration-instance-sg \
  --description "Security group for Redis Cloud migration EC2 instance" \
  --vpc-id $APP_VPC_ID \
  --query 'GroupId' \
  --output text)

# Allow SSH access from anywhere (IPv4 and IPv6)
aws ec2 authorize-security-group-ingress \
  --group-id $REDISSHAKE_SG_ID \
  --ip-permissions '[{"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"0.0.0.0/0"}],"Ipv6Ranges":[{"CidrIpv6":"::/0"}]}]'
```

3. Create an EC2 instance:

```bash
# Create key pair if needed
aws ec2 create-key-pair \
  --key-name redis-cloud-migration-key \
  --query 'KeyMaterial' \
  --output text > redis-cloud-migration-key.pem

chmod 400 redis-cloud-migration-key.pem

# Launch instance with public IP
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id ami-085ad6ae776d8f09c \
  --instance-type t2.medium \
  --subnet-id $APP_SUBNET_ID \
  --security-group-ids $REDISSHAKE_SG_ID \
  --associate-public-ip-address \
  --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
  --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
  --count 1 \
  --key-name redis-cloud-migration-key \
  --user-data '#!/bin/bash
yum update -y
yum install -y docker
systemctl start docker
systemctl enable docker

# install redis-cli
amazon-linux-extras install epel -y
yum install -y redis' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=redis-cloud-migration-instance}]' \
  --query 'Instances[0].InstanceId' \
  --output text)

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
```

4. Connect to the instance:
```bash
# SSH into the instance using your preferred method based on your infrastructure setup
ssh -i redis-cloud-migration-key.pem ec2-user@$PUBLIC_IP
```

### 2. Configure Migration

1. Test connection to Redis Cloud:

<Tabs defaultValue={typeof window !== 'undefined' ?
  (new URLSearchParams(window.location.search).get('cluster') === 'true' ? 'cluster-node' : 'single-node')
  : 'cluster-node'}>

<TabItem value="cluster-node" label="Cluster Node">

```bash
# Test connection to Redis Cloud cluster
redis-cli -h $REDIS_CLOUD_URL -p $REDIS_CLOUD_PORT -a $REDIS_CLOUD_PASSWORD -c ping
```

</TabItem>
<TabItem value="single-node" label="Single Node">

```bash
# Test connection to Redis Cloud single node
redis-cli -h $REDIS_CLOUD_URL -p $REDIS_CLOUD_PORT -a $REDIS_CLOUD_PASSWORD ping
```

</TabItem>
</Tabs>

2. Create redis-shake configuration file:

<Tabs defaultValue={typeof window !== 'undefined' ?
  (new URLSearchParams(window.location.search).get('cluster') === 'true' ? 'cluster-node' : 'single-node')
  : 'cluster-node'}>
<TabItem value="cluster-node" label="Cluster Node">

```bash
cat << EOF > redis-shake.toml
[scan_reader]
cluster = true
address = "${REDIS_CLOUD_URL}:${REDIS_CLOUD_PORT}"
password = "${REDIS_CLOUD_PASSWORD}"
tls = true
ksn = true

[redis_writer]
cluster = true
# if public datastore, use 6385 port
address = "${DRAGONFLY_CLOUD_URL}:6379"
username = "default"
password = "${DRAGONFLY_CLOUD_PASSWORD:-}"
tls = true

[advanced]
log_level = "debug"
EOF
```

</TabItem>
<TabItem value="single-node" label="Single Node">

```bash
cat << EOF > redis-shake.toml
[scan_reader]
cluster = false
address = "${REDIS_CLOUD_URL}:${REDIS_CLOUD_PORT}"
password = "${REDIS_CLOUD_PASSWORD}"
tls = true
ksn = true

[redis_writer]
cluster = false
# if public datastore, use 6385 port
address = "${DRAGONFLY_CLOUD_URL}:6379"
username = "default"
password = "${DRAGONFLY_CLOUD_PASSWORD:-}"
tls = true

[advanced]
log_level = "debug"
EOF
```

</TabItem>
</Tabs>

Note: Since Redis Cloud doesn't support PSYNC, we use the SCAN-based migration approach which is slower but more reliable.

### 3. Run Migration

Run redis-shake using Docker:

```bash
docker run -v "$(pwd)/redis-shake.toml:/redis-shake-config.toml" \
--entrypoint ./redis-shake \
ghcr.io/tair-opensource/redisshake:latest \
/redis-shake-config.toml
```

The container will:
1. Connect to Redis Cloud using the public endpoint
2. Connect to Dragonfly Cloud through the peered VPC
3. Start scanning and copying data
4. Show progress in real-time in the form of logs

### 4. Verify Migration

After the migration completes:

1. Check the container logs for any errors
2. Compare key counts:
```bash
# On source (Redis Cloud)
redis-cli -h $REDIS_CLOUD_URL -p $REDIS_CLOUD_PORT -a $REDIS_CLOUD_PASSWORD dbsize

# On target (Dragonfly Cloud)
redis-cli -h $DRAGONFLY_CLOUD_URL -p 6379 -a "${DRAGONFLY_CLOUD_PASSWORD:-}" dbsize
```
3. Sample a few keys to verify data integrity

## Cutover Strategy

Before switching your application to use Dragonfly Cloud, Make sure to have confirmed that the migraiton is
successful and that the data has all been caught up.

## Post-Migration

1. Make sure to have updated all your application configurations to point to the new Dragonfly Cloud endpoint
2. Monitor application performance and behavior
3. Clean up:

```bash
# clean up the EC2 instance
aws ec2 terminate-instances --instance-ids $INSTANCE_ID

# clean up the security group
aws ec2 delete-security-group --group-id $REDISSHAKE_SG_ID

# clean up the key pair
aws ec2 delete-key-pair --key-name redis-cloud-migration-key
```
