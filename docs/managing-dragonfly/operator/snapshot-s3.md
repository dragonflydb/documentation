# Configure Snapshots to S3 with the Dragonfly Operator

In this guide, We will see how to configure the Dragonfly Instances to use S3 as a backup location with the
Dragonfly Operator. While just having the AWS credentials in the environment (through a file or env) is enough
to use S3, In this guide we will use [AWS IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) to provide the credentials to the Dragonfly
pod.

As this mechanism uses OIDC (OpenID Connect) to authenticate the service account, we will also get the benefits of
credentials isolation and automatic rotation of credentials. This way we can avoid having to pass long lived credentials. This is all done automatically by EKS.

Alternatively, you can use [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) to provide credentials to the Dragonfly pod. EKS Pod Identity is a newer mechanism that simplifies the process of associating IAM roles with Kubernetes service accounts, without requiring an OIDC provider.

## Prerequisites

- A Kubernetes cluster with [Dragonfly installed](./installation.md)

## Create an EKS cluster

```bash
eksctl create cluster --name df-s3 --region us-east-1  
```

## Create and Associate IAM OIDC Provider for your cluster

By following the [AWS documentation](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html), create and associate an IAM OIDC provider for your cluster.

This is a required step for the next steps to work.

## Create an S3 bucket

Now, we will create an S3 bucket to store the snapshots. This bucket can be created using the AWS console or using the AWS CLI.

```bash
aws s3 mb s3://df-s3 
```

## Create a policy to read a specific S3 bucket

We will now create a policy that allows the Dragonfly Instance to read and write to the S3 bucket we created in the previous step.

```bash
cat <<EOF > policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::df-s3/*",
                "arn:aws:s3:::df-s3"
            ]
        }
    ]
}
EOF
```

```bash
aws iam create-policy --policy-name dragonfly-backup --policy-document file://policy.json
```

## Associate the policy with a role

Now, we will associate the policy we created in the previous step with a role. This role will be used by the service account called `dragonfly-backup` which will also be created in this step.

Replace `<account-no>` with your AWS account number.

```bash
eksctl create iamserviceaccount --name dragonfly-backup --namespace default --cluster df-s3 --role-name dragonfly-backup --attach-policy-arn arn:aws:iam::<account-no>:policy/dragonfly-backup --approve
```

### Using EKS Pod Identity (Alternative)

If you prefer to use EKS Pod Identity instead of IAM roles for service accounts, you can associate the IAM role with the service account using the EKS Pod Identity mechanism. This does not require an OIDC provider.

First, create the IAM role and attach the policy:

```bash
aws iam create-role --role-name dragonfly-backup --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name dragonfly-backup --policy-arn arn:aws:iam::<account-no>:policy/dragonfly-backup
```

Then, create the EKS Pod Identity association:

```bash
aws eks create-pod-identity-association --cluster-name df-s3 --namespace default --service-account dragonfly-backup --role-arn arn:aws:iam::<account-no>:role/dragonfly-backup
```

You will also need to ensure the EKS Pod Identity Agent add-on is installed in your cluster:

```bash
eksctl create addon --name eks-pod-identity-agent --cluster df-s3 --region us-east-1
```

## Create a Dragonfly Instance with that service account

Let's create a Dragonfly Instance with the service account we created in the previous step. We will also configure the snapshot location to be the S3 bucket we created in the previous steps.

```bash
kubectl apply -f - <<EOF
apiVersion: dragonflydb.io/v1alpha1
kind: Dragonfly
metadata:
  name: dragonfly-sample
spec:
  replicas: 1
  serviceAccountName: dragonfly-backup
  snapshot:
    dir: "s3://df-s3"
EOF
```

## Verify that the Dragonfly Instance is running

```bash
kubectl describe dragonfly dragonfly-sample
```

## Load Data and Terminate the Dragonfly Instance

Now, we will load some data into the Dragonfly Instance and then terminate the Dragonfly Instance.

```bash
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-sample.default SET 1 2
```

```bash
kubectl delete pod dragonfly-sample-0
```

## Verification

### Verify that the backups are created in the S3 bucket

```bash
aws s3 ls s3://df-s3
```

### Verify that the data is automatically restored

```bash
kubectl run -it --rm --restart=Never redis-cli --image=redis:7.0.10 -- redis-cli -h dragonfly-sample.default GET 1
```

As you can see, the data is automatically restored from the S3 bucket. This is because the Dragonfly instance is configured to use the S3 bucket as the snapshot location.
