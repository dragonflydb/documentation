---
title: AWS ElastiCache
description: The following guide will help you migrate from AWS ElastiCache to Dragonfly Cloud
sidebar_position: 1
---

# From AWS Elasticache

*Note: This guide applies to migrating both Redis and Valkey workloads from AWS ElastiCache to Dragonfly Cloud. The migration process is the same regardless of which engine you're currently using on ElastiCache.*

## Prerequisites

Before starting the migration, ensure you have:

1. Access to your AWS ElastiCache cluster from the application's VPC (APP_VPC_ID)
2. A Dragonfly Cloud Network peered with your application's VPC (APP_VPC_ID)
3. A Dragonfly Cloud Datastore in the private network.
4. AWS CLI configured with appropriate permissions

## Migration Steps

### 1. Launch EC2 Instance in Application VPC

1. Get your application VPC and subnet information:
   ```bash
   # Set the ElastiCache cluster Name and Application VPC details
   CLUSTER_NAME=<your-cluster-name>
   APP_VPC_ID=<your-application-vpc-id>  # VPC where your application and ElastiCache reside
   APP_SUBNET_ID=<your-application-subnet-id>  # Private subnet where your application runs

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

   # Allow SSH access based on your security requirements
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

4. Create an EC2 instance in your application's private subnet:
   ```bash
   # Create key pair if needed
   aws ec2 create-key-pair \
     --key-name elasticache-migration-key \
     --query 'KeyMaterial' \
     --output text > elasticache-migration-key.pem

   chmod 400 elasticache-migration-key.pem

   # Launch instance in the private subnet
   INSTANCE_ID=$(aws ec2 run-instances \
     --image-id ami-085ad6ae776d8f09c \
     --instance-type t2.medium \
     --subnet-id $APP_SUBNET_ID \
     --security-group-ids $REDISSHAKE_SG_ID \
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

Monitor the progress of the migration by following the logs of the container.

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
