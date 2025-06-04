---
sidebar_position: 2
---

import PageTitle from '@site/src/components/PageTitle';

# GCP Cloud Run

<PageTitle title="Connecting from GCP Cloud Run | Dragonfly Cloud" />

[GCP Cloud Run](https://cloud.google.com/run) is a serverless compute service provided by Google Cloud Platform (GCP).
It allows you to run code without provisioning or managing servers.
It supports various programming languages and integrates seamlessly with other GCP services,
making it ideal for building scalable, event-driven applications.

This guide explains how to create a Cloud Run function that connects to a Dragonfly Cloud data store.
Note that Cloud Run is the fully managed serverless platform,
whereas a [Cloud Run function](https://cloud.google.com/blog/products/serverless/google-cloud-functions-is-now-cloud-run-functions)
is a deployment option that allows you to deploy inline code scripts (aka. functions) instead of container images
or code repositories directly on the Cloud Run platform.

---

## Prerequisites

1. **Dragonfly Cloud Data Store**: Ensure you have a running [Dragonfly Cloud](https://dragonflydb.cloud/) data store and its connection URI.
2. **GCP Console**: Access to Cloud Run and IAM services.
3. **Go Toolchain**: In this guide, the Cloud Run service will be written in Go.
4. **Redis Client Library**: Use the `go-redis` package to interact with Dragonfly.

---

## Cloud Run function code

I am writing a function for this guide for simplicity. You can deploy a service
instead. The process to connect to a dragonfly data store is same. I will deploy
the below sample code -

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

var addr string
var pass string

func init() {
   functions.HTTP("HelloHTTP", helloHTTP)
}

// helloHTTP is an HTTP Cloud Function with a request parameter.
func helloHTTP(w http.ResponseWriter, r *http.Request) {
  var d struct {
    Name string `json:"name"`
  }
  if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
    fmt.Fprint(w, "Hello, World!")
    return
  }

  setDragonflyValue(d.Name)
  if d.Name == "" {
    fmt.Fprint(w, "Hello, World!")
    return
  }
  fmt.Fprintf(w, "Hello, %s!", html.EscapeString(d.Name))
}

func setDragonflyValue(name string) {
    ctx := context.Background()
    addr = os.Getenv("DFADDR") // format- <datastore-host>:<port>
    pass = os.Getenv("DFPASS") // datastore password

    // Create a Redis client
    client := redis.NewClient(&redis.Options{
        Addr:     addr,
        Password: pass,
        DB:       0,    // Use default DB
    })

    // Ping the server to test the connection
    pong, err := client.Ping(ctx).Result()
    if err != nil {
        fmt.Printf("Error connecting to Dragonfly: %v\n", err)
        return
    }
    fmt.Printf("Connected to Dragonfly: %s\n", pong)

    // Perform some test operations
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

    // Close the connection
    err = client.Close()
    if err != nil {
        fmt.Printf("Error closing connection: %v\n", err)
    }
}
```

The code uses two environment variables `DFADDR` and `DFPASS`.

## Steps to Connect from the Cloud Run Function to a public data store

### 1. Create a New Cloud Run Function

1. Go to the [Cloud Run](https://console.cloud.google.com/run).
2. Click **Write a function**.
3. Choose **Go Runtime**.
4. Provide a name for your function (e.g., `DragonflyConnector`).
5. Expand the Containers section.
6. Edit the **Container Port** to match with the data store's port.
7. Add `DFADDR` and `DFPASS` environment variables.
8. Click **Create**.

### 2. Test the Cloud Run Function

1. Click the **Test** button in the console.
2. Create a new test event (you can use the default template).
3. Run the test in cloud shell.
4. Check the logs in **Logs** to verify the connection and the key-value pair operation.

---

## Connect to a Private Datastore

Private datastores are hosted within a Virtual Private Cloud (VPC), which provides
an isolated network environment. To enable your Cloud Run function to securely
connect to a private Dragonfly datastore, follow these beginner-friendly steps:

### 1. Set Up VPC Peering

1. Create a VPC in your GCP account within the same region as your datastore.
2. Establish a peering connection between your VPC and the datastore's VPC. This allows the two networks to communicate. For detailed guidance, refer to the [VPC Peering Connections documentation](../../connections.md).

### 2. Adjust Firewall Rules

1. Open the [VPC Network Console](https://console.cloud.google.com/networking/networks/list).
2. Select your network and open the Firewall settings.
3. Add an ingress rule to allow traffic from your datastore vpc. Put datastore vpc CIDR range in the Source Ipv4 range field. Allow all ports.

### 3. Edit Cloud Run settings

As the data store is private, you need to configure your cloud run service's network setting to the
VPC network you just created.

1. Go to the [Cloud Run](https://console.cloud.google.com/run). Select your service.
2. Navigate to the **Networking** tab.
3. Select **Internal Ingress**. Save changes.
4. Once deployed, click **Edit & deploy new version**.
5. Edit container port to your datastore's port. Update `DFADDR` and `DFPASS` (empty if passkey is not set).
6. Go to **Networking**. Select **Connect to a VPC for outbound traffic**. Choose your vpc.
7. Deploy the changes.

### 4. Test the Connection

1. Click **Test**. Copy the test command.
2. You need to create a vm instance inside your vpc to run the test. Go to **VM instance** tab and
   create a vm instance. Make sure you've configured the network interface to use your vpc.
3. Update your firewall rule so that you can connect to the instance via ssh.
4. SSH to your machine. Run the test command.

You'll see the logs in **Logs** that dragonfly has stored the value.

By following these steps, you can securely connect your Cloud run service to a private Dragonfly datastore, ensuring your application remains both scalable and secure.

---

## Conclusion

You have successfully created a GCP Cloud Run function that connects to Dragonfly Cloud, sets a test key-value pair, and verifies the connection. You can now extend this function to perform more complex operations with Dragonfly.
