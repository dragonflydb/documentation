---
title: AWS ElastiCache
description: The following guide will help you migrate from AWS ElastiCache to Dragonfly Cloud
sidebar_position: 1
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import { ConfigDisplay } from './_migration_options.mdx';

# AWS ElastiCache Migration

In this guide, we will walk you through the steps to migrate from AWS ElastiCache to Dragonfly Cloud.

<ConfigDisplay 
  isCluster={new URLSearchParams(window.location.search).get('cluster') === 'true'} 
  isSync={new URLSearchParams(window.location.search).get('mode') === 'sync'} 
/>

## Prerequisites

Before starting the migration, ensure you have:

1. Access to your AWS ElastiCache cluster from the application's VPC (APP_VPC_ID)
2. A Dragonfly Cloud Network peered with your application's VPC (APP_VPC_ID). Follow the [instructions here](/docs/cloud/connections.md) to peer your VPC with Dragonfly Cloud.
3. A Dragonfly Cloud Datastore in the private network. Follow the [instructions here](/docs/cloud/datastores.md) to create a datastore.
4. AWS CLI configured with appropriate permissions

## Migration Steps

### 1. Launch EC2 Instance in Application VPC 

1. Get your application VPC and subnet information:

```bash
# Set the ElastiCache cluster Name and Application VPC details
CLUSTER_NAME=<your-cluster-name>
APP_VPC_ID=<your-application-vpc-id>  # VPC where your application and ElastiCache reside and Dragonfly Cloud is peered
APP_SUBNET_ID=<your-application-subnet-id>  # Subnet where we can access both ElastiCache and Dragonfly Cloud

# Set the Dragonfly Cloud Datastore details
DRAGONFLY_CLOUD_URL=<your-dragonfly-cloud-url>
DRAGONFLY_CLOUD_PASSWORD=<your-dragonfly-cloud-password>
```

2. Create security group for migration instance:

```bash
# Create security group
REDISSHAKE_SG_ID=$(aws ec2 create-security-group \
  --group-name migration-instance-sg \
  --description "Security group for ElastiCache migration EC2 instance" \
  --vpc-id $APP_VPC_ID \
  --query 'GroupId' \
  --output text)

# Allow SSH access from anywhere (IPv4 and IPv6)
aws ec2 authorize-security-group-ingress \
  --group-id $REDISSHAKE_SG_ID \
  --ip-permissions '[{"IpProtocol":"tcp","FromPort":22,"ToPort":22,"IpRanges":[{"CidrIp":"0.0.0.0/0"}],"Ipv6Ranges":[{"CidrIpv6":"::/0"}]}]'
```

3. Allow EC2 instance from the migration security group to access ElastiCache:

```bash
# Get ElastiCache security group ID
ELASTICACHE_SG_ID=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id $CLUSTER_NAME \
  --query 'CacheClusters[0].SecurityGroups[0].SecurityGroupId' \
  --output text)

# Allow access from migration security group
aws ec2 authorize-security-group-ingress \
  --group-id $ELASTICACHE_SG_ID \
  --protocol tcp \
  --port 6379 \
  --source-group $REDISSHAKE_SG_ID
```

4. Create an EC2 instance:

```bash
# Create key pair if needed
aws ec2 create-key-pair \
  --key-name elasticache-migration-key \
  --query 'KeyMaterial' \
  --output text > elasticache-migration-key.pem

chmod 400 elasticache-migration-key.pem

# Launch instance with public IP
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id ami-085ad6ae776d8f09c \
  --instance-type t2.medium \
  --network-interfaces "[{\"AssociatePublicIpAddress\":true,\"DeviceIndex\":0,\"Groups\":[\"$REDISSHAKE_SG_ID\"]}]" \
  --key-name elasticache-migration-key \
  --user-data '#!/bin/bash
  yum update -y
  yum install -y docker
  systemctl start docker
  systemctl enable docker
  
  # install redis-cli
  amazon-linux-extras install epel -y
  yum install -y redis' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=elasticache-migration-instance}]' \
  --query 'Instances[0].InstanceId' \
  --associate-public-ip-address \
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

5. Connect to the instance:
```bash
# SSH into the instance using your preferred method based on your infrastructure setup
ssh -i elasticache-migration-key.pem ec2-user@$PUBLIC_IP
```

### 2. Configure Migration

0. Retrieve the ElastiCache endpoint and auth details:
```bash
# Get cluster endpoint
ELASTICACHE_ENDPOINT=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id $CLUSTER_NAME \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
  --show-cache-node-info \
  --output text)

# For cluster mode, get all node endpoints
CLUSTER_ENDPOINTS=$(aws elasticache describe-replication-groups \
  --replication-group-id $CLUSTER_NAME \
  --query 'ReplicationGroups[0].NodeGroups[0].NodeGroupMembers[*].ReadEndpoint.Address' \
  --output text | tr '\t' ',')

# Check if authentication is enabled
AUTH_TOKEN=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id $CLUSTER_NAME \
  --query 'CacheClusters[0].AuthTokenEnabled' \
  --output text)

if [ "$AUTH_TOKEN" = "true" ]; then
  echo "Authentication is enabled. You'll need to retrieve the auth token from AWS Secrets Manager or your secure storage."
else
  echo "Authentication is not enabled"
fi

# Test connection (for TLS enabled clusters)
docker run -it redis redis-cli -h $ELASTICACHE_ENDPOINT -p 6379 --tls --insecure -c ping
# For non-TLS clusters, use:
docker run -it redis redis-cli -h $ELASTICACHE_ENDPOINT -p 6379 -c ping
```

1. Create redis-shake configuration file:

Choose the appropriate configuration based on your ElastiCache setup:

<Tabs defaultValue={typeof window !== 'undefined' ? 
  (new URLSearchParams(window.location.search).get('cluster') === 'true' ? 
    (new URLSearchParams(window.location.search).get('mode') === 'sync' ? 'cluster-sync' : 'cluster-scan') :
    (new URLSearchParams(window.location.search).get('mode') === 'sync' ? 'single-node-sync' : 'single-node-scan')
  ) : 'single-node-sync'}>
<TabItem value="single-node-sync" label="Single-Node + SYNC">

For single-node mode with PSYNC enabled on ElastiCache:

```toml
[sync_reader]
cluster = false
address = "$ELASTICACHE_ENDPOINT:6379"
tls = true

[redis_writer]
cluster = false
address = "$DRAGONFLY_CLOUD_URL:6379"
username = "default"
password = "$DRAGONFLY_CLOUD_PASSWORD"
tls = true
```

</TabItem>
<TabItem value="cluster-sync" label="Cluster + SYNC">

For cluster mode with PSYNC enabled on ElastiCache:

```toml
[sync_reader]
cluster = true
address = "$CLUSTER_ENDPOINTS"
tls = true

[redis_writer]
cluster = true
address = "$DRAGONFLY_CLOUD_URL:6379"
username = "default"
password = "$DRAGONFLY_CLOUD_PASSWORD"
tls = true
```

</TabItem>
<TabItem value="single-node-scan" label="Single-Node + SCAN">

For single-node mode without PSYNC enabled:

```toml
[scan_reader]
cluster = false
address = "$ELASTICACHE_ENDPOINT:6379"
tls = true

[redis_writer]
cluster = false
address = "$DRAGONFLY_CLOUD_URL:6379"
username = "default"
password = "$DRAGONFLY_CLOUD_PASSWORD"
tls = true

[advanced]
log_level = "debug"
```

</TabItem>
<TabItem value="cluster-scan" label="Cluster + SCAN">

For cluster mode without PSYNC enabled:

```toml
[scan_reader]
cluster = true
address = "$CLUSTER_ENDPOINTS"
tls = true

[redis_writer]
cluster = true
address = "$DRAGONFLY_CLOUD_URL:6379"
username = "default"
password = "$DRAGONFLY_CLOUD_PASSWORD"
tls = true

[advanced]
log_level = "debug"
```

</TabItem>
</Tabs>

Save the appropriate configuration to `redis-shake.toml`.

### 3. Run Migration

Run redis-shake using Docker:

```bash
docker run -v "$(pwd)/redis-shake.toml:/redis-shake-config.toml" \
--entrypoint ./redis-shake \
ghcr.io/tair-opensource/redisshake:latest \
/redis-shake-config.toml
```

The container will:
1. Connect to ElastiCache (which is now accessible within the VPC)
2. Connect to Dragonfly Cloud
3. Start syncing data
4. Show progress in real-time

### 4. Verify Migration

After the migration completes:

1. Check the container logs for any errors
2. Compare key counts:
```bash
# On source (from EC2 instance)
docker run redis redis-cli -h $ELASTICACHE_ENDPOINT dbsize

# On target
docker run redis redis-cli -h $DRAGONFLY_CLOUD_URL dbsize
```
3. Sample a few keys to verify data integrity


## Live Migration

Now that you have verified the migration, Your application is already pointing to the new Dragonfly Cloud endpoint. Once you have verified that the application is working as expected, you can proceed to terminate the ElastiCache cluster after you have confirmed that the migration is successful and things are working as expected.

## Post-Migration

1. Update your application configurations to point to the new Dragonfly Cloud endpoint
2. Monitor application performance and behavior
3. Keep the ElastiCache cluster as backup until you're confident in the migration
4. Clean up:

```bash
# clean up the EC2 instance
aws ec2 terminate-instances --instance-ids $INSTANCE_ID

# clean up the security group
aws ec2 delete-security-group --group-id $REDISSHAKE_SG_ID

# clean up the key pair
aws ec2 delete-key-pair --key-name elasticache-migration-key
```
