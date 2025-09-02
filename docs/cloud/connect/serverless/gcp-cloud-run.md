---
sidebar_position: 2
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# GCP Cloud Run

<CloudBadge/>
<br/>

<PageTitle title="Connecting from GCP Cloud Run | Dragonfly Cloud" />

This guide explains how to create a GCP Cloud Run function that connects to a Dragonfly Cloud data store.

[GCP Cloud Run](https://cloud.google.com/run) is a serverless compute service provided by Google Cloud Platform (GCP).
It allows you to run code without provisioning or managing servers.
It supports various programming languages and integrates seamlessly with other GCP services,
making it ideal for building scalable, event-driven applications.

Within the Cloud Run service,
a [Cloud Run function](https://cloud.google.com/blog/products/serverless/google-cloud-functions-is-now-cloud-run-functions)
is a deployment option that allows you to deploy inline code scripts or functions directly instead of deploying container images or code repositories.
However, the process to connect to a Dragonfly Cloud data store is generally applicable to both Cloud Run services and functions.

**Note**: You can skip to the [Connecting to a Private Dragonfly Data Store](#connecting-to-a-private-dragonfly-data-store)
section if you already have the Cloud Run function set up and just want to learn how to work with private Dragonfly Cloud data stores.

---

## Prerequisites

1. **Dragonfly Cloud Data Store**: Ensure you have a running [Dragonfly Cloud](https://dragonflydb.cloud/) data store and its connection URI.
2. **GCP Console**: Access to Cloud Run and IAM services.
3. **Go Toolchain**: In this guide, the Cloud Run service will be written in Go.
4. **Redis Client Library**: Use the `go-redis` package to interact with Dragonfly.

---

## Cloud Run Function Example Code

For the purposes of this guide, a Cloud Run function implementation is provided for simplicity.
Alternatively, a Cloud Run service deployment may be used instead.
The connection process to a Dragonfly Cloud data store remains the same in either case.
The following sample code will be deployed:

```go
package helloworld

import (
  "encoding/json"
  "fmt"
  "html"
  "net/http"
  "os"
  "context"

  "github.com/redis/go-redis/v9"
  "github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

func init() {
   functions.HTTP("HelloHTTP", helloHTTP)
}

// An HTTP Cloud Function handler that responds to HTTP requests.
func helloHTTP(w http.ResponseWriter, r *http.Request) {
  var req struct {
    Name string `json:"name"`
  }
  if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
    fmt.Fprint(w, "Hello, World!")
    return
  }

  setDragonflyValue(req.Name)
  if req.Name == "" {
    fmt.Fprint(w, "Hello, World!")
    return
  }
  fmt.Fprintf(w, "Hello, %s!", html.EscapeString(req.Name))
}

func setDragonflyValue(name string) {
    ctx := context.Background()
    connectionURI := os.Getenv("DRAGONFLY_CONNECTION_URI")

    // Dragonfly is compatible with the Redis protocol, we can use existing Redis libraries.
    opt, err := redis.ParseURL(connectionURI)
    if err != nil {
        fmt.Printf("Error parsing Dragonfly connection URI: %v\n", err)
        return
    }
    client := redis.NewClient(opt)

    // Ping the server to test the connection.
    pong, err := client.Ping(ctx).Result()
    if err != nil {
        fmt.Printf("Error connecting to Dragonfly: %v\n", err)
        return
    }
    fmt.Printf("Connected to Dragonfly: %s\n", pong)

    // Perform some test operations.
    err = client.Set(ctx, "test_key", name, 0).Err()
    if err != nil {
        fmt.Printf("Error setting key: %v\n", err)
        return
    }

    value, err := client.Get(ctx, "test_key").Result()
    if err != nil {
        fmt.Printf("Error getting key: %v\n", err)
        return
    }
    fmt.Printf("Retrieved value: %s\n", value)

    // Close the connection.
    err = client.Close()
    if err != nil {
        fmt.Printf("Error closing connection: %v\n", err)
    }
}
```

The example code requires an environment variable named `DRAGONFLY_CONNECTION_URI`.

---

## Connecting to a Public Dragonfly Data Store

### 1. Create a New Cloud Run Function

1. Go to the [Cloud Run](https://console.cloud.google.com/run) console.
2. Click **Write a function**.
3. Provide a name for your function/service (e.g., `HelloDragonfly`).
4. Choose a Go runtime version that supports your function code.
5. Expand the **Container(s)** section and add a new environment variable under the `Variables & Secrets` tab:
   - **Key**: `DRAGONFLY_CONNECTION_URI`
   - **Value**: Your Dragonfly Cloud connection URI (e.g., `rediss://<username>:<password>@<host>:<port>`).
6. Click **Create** to create the function.
7. Add your code or the code provided above to the inline editor and wait for the function to be deployed.

### 2. Test the Cloud Run Function

1. Click the **Test** button in the Cloud Run console.
2. Create a new test event (you can use the default template).
3. Run the test (you can use Cloud Shell for simplicity).
4. Check the logs in **Logs** to verify the connection and the key-value pair operation.

---

## Connecting to a Private Dragonfly Data Store

Private data stores are hosted within a Virtual Private Cloud (VPC), which provides
an isolated network environment. To enable your Cloud Run function to securely
connect to a private Dragonfly Cloud data store, follow these beginner-friendly steps:

### 1. Set Up VPC Peering

1. Create a VPC in your GCP account within the same region as your data store.
2. Establish a peering connection between your VPC and the data store's VPC.
   This allows the two networks to communicate. For detailed guidance, refer to the [VPC Peering Connections documentation](../../connections.md).

### 2. Adjust Firewall Rules

1. Open the [VPC Network Console](https://console.cloud.google.com/networking/networks/list).
2. Select your network and open the **Firewall** settings.
3. Add an ingress rule to allow traffic from your data store VPC. Put the data store VPC CIDR range in the source IPV4 range field, and allow all ports.

### 3. Edit Cloud Run Settings

As the data store is private, you need to configure Cloud Run's network setting
to the VPC network you just created.

1. Go to the [Cloud Run](https://console.cloud.google.com/run). Select your service.
2. Navigate to the **Networking** tab.
3. Select **Internal Ingress**. Save changes.
4. Once deployed, click **Edit & deploy new version**.
5. Make sure the `DRAGONFLY_CONNECTION_URI` environment variable is set to the data store's private connection URI.
6. Go to **Networking**. Select **Connect to a VPC for outbound traffic**. Choose your VPC.
7. Deploy the changes.

### 4. Test the Connection

1. Click **Test**. Copy the test command.
2. You need to create a VM instance inside your VPC to run the test. Go to the **VM instances** tab and
   create a VM instance. Make sure you've configured the network interface to use your VPC.
3. Update your firewall rules so that you can connect to the instance via SSH.
4. SSH to your machine and run the test command.

You'll see in **Logs** that Dragonfly has stored the value.
By following these steps, you can securely connect your Cloud Run service to a private Dragonfly Cloud data store,
ensuring your application remains both scalable and secure.

---

## Conclusion

You have successfully created a GCP Cloud Run function that connects to Dragonfly Cloud,
sets a test key-value pair, and verifies the connection.
You can now extend this function to perform more complex operations with Dragonfly.
