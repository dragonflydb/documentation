---
title: AWS ElastiCache
description: The following guide will help you migrate from AWS ElastiCache to Dragonfly Cloud
sidebar_position: 1
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import { ConfigDisplay } from './\_migration_options.mdx';
import BrowserOnly from '@docusaurus/BrowserOnly';
import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# AWS ElastiCache Migration

<CloudBadge/>
<br /><br />

<PageTitle title="AWS ElastiCache Migration | Dragonfly Cloud" />

In this guide, we will walk you through the steps to migrate from AWS ElastiCache to Dragonfly Cloud.

<BrowserOnly>
{() => (
  <ConfigDisplay 
    isCluster={new URLSearchParams(window.location.search).get('cluster') === 'true'} 
    isSync={new URLSearchParams(window.location.search).get('mode') === 'sync'} 
  />
)}
</BrowserOnly>

:::tip Need Help?
If you have any questions or need assistance with your migration, our team is here to help! Visit our <u>[contact page](https://www.dragonflydb.io/contact)</u> for assistance.
:::

## Prerequisites

Before starting the migration, ensure you have:

1. Access to your AWS ElastiCache cluster from the application's VPC (APP_VPC_ID)
2. A Dragonfly Cloud Network peered with your application's VPC (APP_VPC_ID). Follow the [instructions here](/docs/cloud/connections.md) to peer your VPC with Dragonfly Cloud
3. A Dragonfly Cloud Datastore in the private network. Follow the [instructions here](/docs/cloud/datastores.md) to create a datastore
4. AWS CLI configured with appropriate permissions

## Migration Steps

### 1. Launch EC2 Instance in Application VPC

1. Get your application VPC and subnet information:

```bash
# Set the ElastiCache cluster Name and Application VPC details
CLUSTER_NAME=<your-cluster-name>
APP_VPC_ID=<your-application-vpc-id>  # VPC where your application and ElastiCache reside and Dragonfly Cloud is peered
APP_SUBNET_ID=<your-application-subnet-id>

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
# Get all cache cluster IDs from the replication group
CACHE_CLUSTER_IDS=$(aws elasticache describe-replication-groups \
  --replication-group-id $CLUSTER_NAME \
  --query 'ReplicationGroups[0].MemberClusters[]' \
  --output text)

# Get the ElastiCache security group ID
# Note: By default, all nodes in an ElastiCache cluster share the same security group
ELASTICACHE_SG_ID=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id $(echo $CACHE_CLUSTER_IDS | cut -f1) \
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
  --subnet-id $APP_SUBNET_ID \
  --security-group-ids $REDISSHAKE_SG_ID \
  --associate-public-ip-address \
  --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
  --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' \
  --count 1 \
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

1. Retrieve the ElastiCache endpoint details:

<Tabs defaultValue={typeof window !== 'undefined' ?
(new URLSearchParams(window.location.search).get('cluster') === 'true' ? 'cluster-node' : 'single-node')
: 'cluster-node'}>

<TabItem value="cluster-node" label="Cluster  Node">

For ElastiCache Cluster, Retreive all the Shard Endpoints:

```bash
# Get cluster endpoints
ELASTICACHE_NODE_IDS=$(aws elasticache describe-replication-groups \
  --replication-group-id $CLUSTER_NAME \
  --query 'ReplicationGroups[0].NodeGroups[*].NodeGroupMembers[0].CacheClusterId' \
  --output text)

# Get the endpoint for each node
ELASTICACHE_ENDPOINTS=()
for node_id in $(echo $ELASTICACHE_NODE_IDS | tr ',' '\n'); do
  echo "Getting endpoint for node $node_id"
  ENDPOINT=$(aws elasticache describe-cache-clusters \
    --cache-cluster-id $node_id \
    --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
    --show-cache-node-info \
    --output text)

  PORT=$(aws elasticache describe-cache-clusters \
    --cache-cluster-id $node_id \
    --query 'CacheClusters[0].CacheNodes[0].Endpoint.Port' \
    --show-cache-node-info \
    --output text)

  ELASTICACHE_ENDPOINTS+=("$ENDPOINT:$PORT")
done

# Final Redis Shake Source Endpoint
REDISSHAKE_SOURCE_ENDPOINT=$(IFS=','; echo "${ELASTICACHE_ENDPOINTS[*]}")

echo "REDISSHAKE_SOURCE_ENDPOINT=$REDISSHAKE_SOURCE_ENDPOINT"
```

</TabItem>
<TabItem value="single-node" label="Single Node">

For single node ElastiCache, Retreive the endpoint:

```bash
ELASTICACHE_NODE_ID=$(aws elasticache describe-replication-groups \
  --replication-group-id $CLUSTER_NAME \
  --query 'ReplicationGroups[0].NodeGroups[*].NodeGroupMembers[0].CacheClusterId' \
  --output text)

# Get single node endpoint
ELASTICACHE_ENDPOINT=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id $ELASTICACHE_NODE_ID \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
  --show-cache-node-info \
  --output text)

# Retreive the port
ELASTICACHE_PORT=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id $ELASTICACHE_NODE_ID \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint.Port' \
  --show-cache-node-info \
  --output text)

# Final Redis Shake Source Endpoint
REDISSHAKE_SOURCE_ENDPOINT="$ELASTICACHE_ENDPOINT:$ELASTICACHE_PORT"

echo "REDISSHAKE_SOURCE_ENDPOINT=$REDISSHAKE_SOURCE_ENDPOINT"
```

</TabItem>
</Tabs>

2. Retreive Password if Authentication is enabled:

```bash
# Check if authentication is enabled
AUTH_TOKEN=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id $ELASTICACHE_NODE_ID \
  --query 'CacheClusters[0].AuthTokenEnabled' \
  --output text)

if [ "$AUTH_TOKEN" = "true" ]; then
  echo "Authentication is enabled. You'll need to retrieve the auth token from AWS Secrets Manager or your secure storage."
else
  echo "Authentication is not enabled"
fi
```

3. Test connection to ElastiCache:

<Tabs defaultValue={typeof window !== 'undefined' ?
(new URLSearchParams(window.location.search).get('cluster') === 'true' ? 'cluster-node' : 'single-node')
: 'cluster-node'}>

<TabItem value="cluster-node" label="Cluster  Node">

```bash
# Test connection (for TLS enabled clusters)
for endpoint in $(echo $REDISSHAKE_SOURCE_ENDPOINT | tr ',' '\n'); do
  url_without_port=$(echo $endpoint | cut -d':' -f1)
  echo "Testing connection to $url_without_port"
  sudo docker run -it redis redis-cli -h $url_without_port --tls --insecure -c ping
done

# For non-TLS clusters, use:
for endpoint in $(echo $REDISSHAKE_SOURCE_ENDPOINT | tr ',' '\n'); do
  url_without_port=$(echo $endpoint | cut -d':' -f1)
  echo "Testing connection to $url_without_port"
  sudo docker run -it redis redis-cli -h $url_without_port -c ping
done
```

</TabItem>
<TabItem value="single-node" label="Single Node">

```bash
# Test connection (for TLS enabled single-node)
url_without_port=$(echo $REDISSHAKE_SOURCE_ENDPOINT | cut -d':' -f1)
echo "Testing connection to $url_without_port"
sudo docker run -it redis redis-cli -h $url_without_port --tls --insecure -c ping

# For non-TLS single-node, use:
url_without_port=$(echo $REDISSHAKE_SOURCE_ENDPOINT | cut -d':' -f1)
echo "Testing connection to $url_without_port"
sudo docker run -it redis redis-cli -h $url_without_port -c ping
```

</TabItem>
</Tabs>

1. Create redis-shake configuration file:

Choose the appropriate configuration based on your ElastiCache setup:

<Tabs defaultValue={typeof window !== 'undefined' ?
(new URLSearchParams(window.location.search).get('cluster') === 'true' ?
(new URLSearchParams(window.location.search).get('mode') === 'sync' ? 'cluster-sync' : 'cluster-scan') :
(new URLSearchParams(window.location.search).get('mode') === 'sync' ? 'single-node-sync' : 'single-node-scan')
) : 'single-node-sync'}>
<TabItem value="single-node-sync" label="Single-Node + SYNC">

For single-node mode with PSYNC enabled on ElastiCache:

```bash
cat << EOF > redis-shake.toml
[sync_reader]
cluster = false
address = "${REDISSHAKE_SOURCE_ENDPOINT}"
tls = true

[redis_writer]
cluster = false
# if public datastore, use 6385 port
address = "${DRAGONFLY_CLOUD_URL}:6379"
username = "default"
password = "${DRAGONFLY_CLOUD_PASSWORD:-}"
tls = true
EOF
```

</TabItem>
<TabItem value="cluster-sync" label="Cluster + SYNC">

For cluster mode with PSYNC enabled on ElastiCache:

```bash
cat << EOF > redis-shake.toml
[sync_reader]
cluster = true
address = "${REDISSHAKE_SOURCE_ENDPOINT}"
tls = true

[redis_writer]
cluster = true
# if public datastore, use 6385 port
address = "${DRAGONFLY_CLOUD_URL}:6379"
username = "default"
password = "${DRAGONFLY_CLOUD_PASSWORD:-}"
tls = true
EOF
```

</TabItem>
<TabItem value="single-node-scan" label="Single-Node + SCAN">

For single-node mode without PSYNC enabled:

```bash
cat << EOF > redis-shake.toml
[scan_reader]
cluster = false
address = "${REDISSHAKE_SOURCE_ENDPOINT}"
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
<TabItem value="cluster-scan" label="Cluster + SCAN">

For cluster mode without PSYNC enabled:

```bash
cat << EOF > redis-shake.toml
[scan_reader]
cluster = true
address = "${REDISSHAKE_SOURCE_ENDPOINT}"
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
</Tabs>

The above approach:

1. Uses direct variable expansion with proper quoting
2. Uses parameter expansion with default empty string for optional password

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
4. Show progress in real-time in the form of logs

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

Now that you have verified the data is being synced continuously, you can now proceed to point your application to the new Dragonfly Cloud endpoint. With this, You have successfully migrated your data from ElastiCache to Dragonfly Cloud without any downtime or data loss.

## Post-Migration

1. Make sure to have updated all your application configurations to point to the new Dragonfly Cloud endpoint
2. Monitor application performance and behavior. Make sure that the application is working as expected with the new Dragonfly Cloud endpoint
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
