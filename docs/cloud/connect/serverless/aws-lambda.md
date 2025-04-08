---
sidebar_position: 1
---

import PageTitle from '@site/src/components/PageTitle';

# AWS Lambda

<PageTitle title="Connecting from AWS Lambda | Dragonfly Cloud" />

AWS Lambda is a serverless compute service provided by Amazon Web Services (AWS). It allows you to run code without provisioning or managing servers. You simply upload your code, and Lambda automatically handles the execution, scaling, and availability. It supports various programming languages and integrates seamlessly with other AWS services, making it ideal for building scalable, event-driven applications.

This guide explains how to create an AWS Lambda function that connects to a Dragonfly Cloud instance.

---

## Prerequisites

1. **Dragonfly Cloud Instance**: Ensure you have a running Dragonfly Cloud instance and its connection URI.
2. **AWS Account**: Access to AWS Lambda and IAM services.
3. **Node Runtime**: The Lambda function will be written in NodeJS.
4. **Redis Client Library**: Use the `redis` package to interact with Dragonfly.

---

## Steps to Create the Lambda Function

### 1. Create a New Lambda Function

1. Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Click **Create function**.
3. Choose **Author from scratch**.
4. Provide a name for your function (e.g., `DragonflyConnector`).
5. Click **Create function**.

---

### 2. Add the Dragonfly URI as an Environment Variable

1. In the Lambda function configuration, go to the **Configuration** tab.
2. Select **Environment variables**.
3. Add a new variable:
   - **Key**: `DRAGONFLY_CONNECTION_URI`
   - **Value**: Your Dragonfly Cloud connection URI (e.g., `rediss://<username>:<password>@<host>:<port>`).

---

### 3. Write the Lambda Function Code

Create a module Javascript file (e.g., `index.mjs`) with the following code:

```js
import {createClient} from 'redis';

const redis = createClient({
    url: process.env.DRAGONFLY_CONNECTION_URI
})

await redis.connect()

if (!redis.isReady) {
    console.log("not ready yet")
}

console.log("ready")
export const handler = async (event) => {
    try {
        // Test connection with basic operations
        await redis.set('lambda_test', JSON.stringify({
            timestamp: new Date().toISOString(),
            source: 'AWS Lambda'
        }));
        
        const result = await redis.get('lambda_test');
        
        return {
            statusCode: 200,
            body: JSON.stringify({
                message: 'Successfully connected to Dragonfly',
                data: JSON.parse(result)
            })
        };
    } catch (error) {
        console.error('Dragonfly connection error:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({
                error: 'Connection failed',
                details: error.message
            })
        };
    }
};
```

---

### 4. Build and Deploy the Lambda Function

1. Your directory should look like this:

   ```sh
   index.mjs
   node_modules/
   package.json
   package-lock.json
   ```

2. **Package**: Aws Lambda takes zip file to load the code:

   ```sh
   zip -r dragonfly-lambda.zip .
   ```

3. **Upload to Lambda**:

   - Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
   - In the **Code** section, upload the `dragonfly-lambda.zip` file.

---

### 5. Test the Lambda Function

1. Go to the **Test** tab in the Lambda Console.
2. Create a new test event (you can use the default template).
3. Run the test.
4. Check the logs in **Monitor > Logs** to verify the connection and the key-value pair operation.

---

## Connecting to a Private Dragonfly Data Store

Private data stores are hosted within a Virtual Private Cloud (VPC), which provides an isolated network environment. To enable your AWS Lambda function to securely connect to a private Dragonfly data store, follow these beginner-friendly steps:

### 1. Set Up VPC Peering

1. Create a VPC in your AWS account within the same region as your data store.
2. Establish a peering connection between your VPC and the data store's VPC. This allows the two networks to communicate. For detailed guidance, refer to the [VPC Peering Connections documentation](../../connections.md).

### 2. Adjust Security Group Rules

1. Open the [VPC Console](https://console.aws.amazon.com/vpc/) and locate the security group associated with your vpc.
2. Add an inbound rule to allow traffic from your vpc:
    - **Type**: Custom TCP Rule
    - **Port Range**: `6379` (Dragonfly port).
    - **Source**: CIDR of the private network.

### 3. Grant Lambda the Necessary Permissions

To allow Lambda to interact with your VPC, you need to update its execution role:

1. Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Select your Lambda function and navigate to the **Configuration** tab.
3. Under **Permissions**, click the execution role name.
4. Add the **AmazonEC2FullAccess** permission to the role. This ensures Lambda can connect to your VPC.

### 4. Configure Lambda to Use the VPC

1. In the [AWS Lambda Console](https://console.aws.amazon.com/lambda/), select your function.
2. Go to the **Configuration** tab and choose **VPC**.
3. Click **Edit** and set the following:
    - **VPC**: Select the VPC you created.
    - **Subnets**: Choose subnets with access to the data store.
    - **Security Groups**: Select the security group that allows traffic to the data store.

### 5. Test the Connection

1. Deploy your Lambda function as described earlier.
2. Update the `DRAGONFLY_CONNECTION_URI` environment variable with the private data store's connection URL.
3. Run a test event in the Lambda Console.
4. Check the logs or query the data store to confirm the connection is successful.

By following these steps, you can securely connect your Lambda function to a private Dragonfly data store, ensuring your application remains both scalable and secure.

## Conclusion

You have successfully created an AWS Lambda function that connects to Dragonfly Cloud, sets a test key-value pair, and verifies the connection. You can now extend this function to perform more complex operations with Dragonfly.
