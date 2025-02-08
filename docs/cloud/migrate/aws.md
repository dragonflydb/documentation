---
title: AWS ElastiCache
description: The following guide will help you migrate from AWS ElastiCache to Dragonfly Cloud
sidebar_position: 1
---

# From AWS Elasticache

*Note: This guide applies to migrating both Redis and Valkey workloads from AWS ElastiCache to Dragonfly Cloud. The migration process is the same regardless of which engine you're currently using on ElastiCache.*

## Prerequisites

Before starting the migration, ensure you have:

1. Access to your AWS ElastiCache cluster
2. Your Dragonfly Cloud instance URL and credentials
3. AWS CLI configured with appropriate permissions
4. The VPC ID, subnet, and security group ID of your ElastiCache cluster

## Migration Steps

### 1. Launch EC2 Instance

1. Get ElastiCache VPC information and create public subnet:
   ```bash
   # Set the ElastiCache cluster Name
   CLUSTER_NAME=<your-cluster-name>

   # Get ElastiCache VPC info
   ELASTICACHE_SUBNET_GROUP=$(aws elasticache describe-cache-clusters \
     --cache-cluster-id $CLUSTER_NAME \
     --query 'CacheClusters[0].CacheSubnetGroupName' \
     --output text)

   VPC_ID=$(aws elasticache describe-cache-subnet-groups \
     --cache-subnet-group-name $ELASTICACHE_SUBNET_GROUP \
     --query 'CacheSubnetGroups[0].VpcId' \
     --output text)

   # Create public subnet in non-overlapping range
   PUBLIC_SUBNET_ID=$(aws ec2 create-subnet \
     --vpc-id $VPC_ID \
     --cidr-block 10.0.0.192/26 \
     --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=migration-public-subnet}]' \
     --query 'Subnet.SubnetId' \
     --output text)

   # Create and attach internet gateway
   IGW_ID=$(aws ec2 create-internet-gateway \
     --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=migration-igw}]' \
     --query 'InternetGateway.InternetGatewayId' \
     --output text)

   aws ec2 attach-internet-gateway \
     --internet-gateway-id $IGW_ID \
     --vpc-id $VPC_ID

   # Create a new route table for the public subnet
   ROUTE_TABLE_ID=$(aws ec2 create-route-table \
     --vpc-id $VPC_ID \
     --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=migration-public-rt}]' \
     --query 'RouteTable.RouteTableId' \
     --output text)

   # Add route to internet
   aws ec2 create-route \
     --route-table-id $ROUTE_TABLE_ID \
     --destination-cidr-block 0.0.0.0/0 \
     --gateway-id $IGW_ID

   # Associate route table with public subnet
   aws ec2 associate-route-table \
     --route-table-id $ROUTE_TABLE_ID \
     --subnet-id $PUBLIC_SUBNET_ID

   echo "VPC ID: $VPC_ID"
   echo "Public Subnet ID: $PUBLIC_SUBNET_ID"
   ```

2. Create a key pair and security group:
   ```bash
   # Create key pair
   aws ec2 create-key-pair \
     --key-name elasticache-migration-key \
     --query 'KeyMaterial' \
     --output text > elasticache-migration-key.pem

   chmod 400 elasticache-migration-key.pem

   # Create security group
   REDISSHAKE_SG_ID=$(aws ec2 create-security-group \
     --group-name migration-instance-sg \
     --description "Security group for ElastiCache migration EC2 instance" \
     --vpc-id $VPC_ID \
     --query 'GroupId' \
     --output text)

   # Allow SSH access from anywhere
   aws ec2 authorize-security-group-ingress \
     --group-id $REDISSHAKE_SG_ID \
     --protocol tcp \
     --port 22 \
     --cidr 0.0.0.0/0

   # Allow all outbound traffic
   aws ec2 authorize-security-group-egress \
     --group-id $REDISSHAKE_SG_ID \
     --protocol all \
     --port -1 \
     --cidr 0.0.0.0/0
   ```

3. Allow EC2 instance to access ElastiCache:
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
   # Launch instance in the public subnet
   INSTANCE_ID=$(aws ec2 run-instances \
     --image-id ami-085ad6ae776d8f09c \
     --instance-type t2.medium \
     --subnet-id $PUBLIC_SUBNET_ID \
     --security-group-ids $REDISSHAKE_SG_ID \
     --key-name elasticache-migration-key \
     --associate-public-ip-address \
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
   ssh -i elasticache-migration-key.pem -v ec2-user@$PUBLIC_IP
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
   # docker run -it redis redis-cli -h $ELASTICACHE_ENDPOINT -p 6379 -c ping
   ```

1. Create redis-shake configuration file:
   ```bash
cat > redis-shake.toml << EOF
[scan_reader]
cluster = true
address = "$ELASTICACHE_ENDPOINT:6379"
tls = true

[redis_writer]
cluster = false
address = "$DRAGONFLY_CLOUD_URL:6385"
username = "default"
password = "$DRAGONFLY_CLOUD_PASSWORD"
tls = true

[advanced]

log_level = "debug"
EOF
```

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

### 4. Monitor Progress

Monitor the Docker container logs:
```bash
docker ps  # Get the container ID
docker logs -f <container-id>
```

### 5. Verify Migration

After the migration completes:

1. Check the container logs for any errors
2. Compare key counts:
   ```bash
   # On source (from EC2 instance)
   docker run redis redis-cli -h <elasticache-endpoint> dbsize
   
   # On target
   docker run redis redis-cli -h <dragonfly-cloud-url> dbsize
   ```
3. Sample a few keys to verify data integrity

## Post-Migration

1. Update your application configurations to point to the new Dragonfly Cloud endpoint
2. Monitor application performance and behavior
3. Keep the ElastiCache cluster as backup until you're confident in the migration
4. Clean up:
   ```bash
   # Terminate EC2 instance when done
   aws ec2 terminate-instances --instance-ids <your-instance-id>
   ```
