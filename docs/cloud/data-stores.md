---
sidebar_position: 2
---

# Data Stores

## Overview

A [Dragonfly Cloud](https://dragonflydb.cloud/) data store represents an endpoint for storing and retrieving in-memory
data, which is compatible with the Redis (RESP2 and RESP3) and the Memcached protocols. The endpoint is a fully managed
service that is backed by one or more Dragonfly server instances. The data store can be accessed from the public
internet or over a private network.

On this page you will find information on how to create, configure, and connect to a Dragonfly Cloud data store.

## Creating a Data Store

- To create a data store, on the **Data Stores** tab,
  click the [+Data Store](https://dragonflydb.cloud/datastores/new) button.
- The minimum configuration consists of a **Name**, a **Cloud Provider**, a **Cloud Region**, and a **Plan**.
- The following cloud providers are supported:
    - Amazon Web Services (AWS)
    - Google Cloud Platform (GCP)
    - Microsoft Azure (private beta, please contact support if you would like to run Dragonfly on Azure)
- Note that the **Cloud Provider** and **Cloud Region** can **NOT** be modified once the data store is created.
- The **Plan** specifies the provisioned memory size and the CPU-to-memory ratio for the data store.
  Available plans are:
    - **Standard**: This plan is suitable for moderate workloads. It provides a balanced CPU-to-memory ratio.
    - **Enhanced**: This plan is suitable for workloads that require more CPU resources.
      It provides **2x the CPU** for the same amount of provisioned memory compared to the **Standard** plan.
    - **Extreme**: This plan is suitable for workloads that require extremely high compute resources.
      It provides **4x the CPU** for the same amount of provisioned memory compared to the **Standard** plan.
- For network bandwidth limits, please refer to the [network bandwidth](./network-bandwidth.md) section.
- You **can** modify the data store **Plan** (memory size, CPU resources) later
  with **zero downtime** to easily scale up or down.

### Advanced Configurations

- By default, the data store will be configured with a **public endpoint**, **TLS**, and an auto-generated **passkey**,
  meaning you can securely connect to it from anywhere over the public internet.
- To create a data store with a **private endpoint**, see [security](#security), [networks](./networks.md),
  and [peering connections](./peering-connections.md).
- By default, the data store will consist of a single Dragonfly server instance.
  To create a highly available data store, read more about high availability [below](#high-availability).
  For cluster mode, please see [cluster mode](#cluster-mode) below.

### After Creating a Data Store

- Once the data store is created, clicking the data store row will open a drawer with the data store configuration,
  including the auto-generated passkey and a Redis-compatible **Connection URI**.
- Once the data store's **Status** becomes **Active**, you can try accessing it with Redis CLI,
  for instance, `redis-cli -u <Connection_URI> PING`.
  Read more information on [how to connect to the data store](#connecting-to-data-store) below.

### Updating the Data Store Configuration

- To update the data store configuration,
  click three-dot
  menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>)
  in the data store row
  and then select **Edit**.
- **Dragonfly Cloud performs data store updates with zero downtime**.

---

## Security

Dragonfly Cloud supports using both public and private endpoints for data access.

### Public Endpoint

With a public endpoint you can connect to the data store from anywhere over the internet.
To protect your data store from unauthorized access public endpoints are configured with *passkey* and *TLS* enabled.   
*TLS* has some performance impact so can be disabled but it is highly recommended to leave it enabled.  
*Passkey* is mandatory and can not be disabled for public endpoints

### Private Endpoint

*Private endpoint* provides better security, performance and lower latency as the data transports to and from the data
stores over private networks and not via the public internet.  
Using a private endpoint also reduces data transfer costs applied by the cloud provider.

In order to create a data store with a private endpoint, you must first create a private network,
see [Networks](./networks) for more information.
Once you have created a private network, you can select it in the *Endpoint* dropdown box when creating a data store.

> ***Tip:*** In order to completely avoid data transfer charges, place your data store in the same availability zone of
> your application. See [High Availability](#high-availability) for specifying the data store availability zone.

*TLS* and *passkey* are disabled by default for private endpoint datastores, but can be enabled.

## Durability and High Availability

### Eviction Policy

Eviction policy controls the behavior of the datastore when it maxes out its memory.  
**No Eviction** - Items are never evicted and out of memory errors are returned when the data store is full.  
**Cache** - The data store behaves as cache and evicts items to free space for new ones when the data store is full.

### High Availability

By default the data store will consist of a single Dragonfly server, this means that in case of software failures,
hardware failures or cloud zone outages data is lost and the data store may be completely unavailable.

To increase availability of your data store you can configure it to be deployed in up to three different zones, one
primary zone for the master and up to two replica zones.
Dragonfly Cloud automatically detects failures and performs failover to an available replica.

To add a replica, expand the *Durability & High Availability* section and click the *Add Replica* button and select the
zone for the replica.
You can select the same zone as the master or a different zone.
When selecting a different zone, inter zone data transfer costs may apply.

***Tip:*** You can also select a zone for the data store master, select the same zone as your application to avoid data
transfer costs.

You can update the data store replica and zones anytime with zero downtime.

## Specializations

**BullMQ** - Enable this for running BullMQ workloads, this requires you to apply Redis Cluster curly braces syntax for
the queue names as described [here](/docs/integrations/bullmq.md).

If that is not possible please contact support.

**Memcached** - Enable this for running Memcached workloads, memcached protocol will be enabled on port 6371.  
*Note*: The memcached protocol does not support authentication, so can be enabled only
for [private endpoint](#private-endpoint) data stores.

**Sidekiq** - Enable this for running Sidekiq workloads, [read more](/docs/integrations/sidekiq.md).

## Cluster Mode

By default a dragonfly cloud data store support redis cluster protocol and clients so you can seamlessly migrate from
redis cluster.

Multi node cluster is in private beta,
please [schedule a meeting with a product expert](https://calendly.com/d/ymz-yhv-q8f/dragonfly-cloud?month=2024-07) to
get access.

---

## Connecting to Data Store

Once a data store *Status* is *Active* you can connect to it with any Redis client using the *Connection URI* provided
in the data store drawer (e.g. rediss://default:h6blm92XXXsa@52tyg3xkp.dragonflydb.cloud:6385).
Here are a few popular examples:

### Redis CLI

1. Install redis-cli, `sudo apt install redis-tools`
2. With the *Connection URI* from the data store drawer execute redis-cli in the terminal e.g.
   `redis-cli -u <connection URI> PING`

### Node.js

1. Install the redis npm package, `npm install redis`
2. Use the following code snippet to connect to the data store

```javascript
import {createClient} from 'redis';

const client = createClient({url: '<connection URI>'});
client.on('connect', () => {
    console.log('Connected to Redis');
});
client.on('error', (err) => {
    console.error('Redis error', err);
});
client.ping((err, res) => {
    if (err) {
        console.error('Error:', err);
        return;
    }
    console.log('Redis PING:', res);
});

```

### Python

1. Install the redis-py package, `pip install redis`
2. Use the following code snippet to connect to the data store

```python
import redis
client = redis.Redis.from_url('<connection URI>')
client.ping()
```

### Go

1. Install the go-redis package, `go get github.com/go-redis/redis/v8`
2. Use the following code snippet to connect to the data store

```go
package main

import (
    "fmt"
	"github.com/go-redis/redis/v8"
)

func main() {
    // Replace "<connection URI>" with the actual connection URI,  
    // <db> is the database number, default is 0
    opt, err := redis.ParseURL("<connection URI>/<db>")
    if err != nil {
	    panic(err)
    }

    client := redis.NewClient(opt)

    pong, err := client.Ping(client.Context()).Result()
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    fmt.Println("Connected to Redis:", pong)
}
```

## ACL Rules

You can leverage [Dragonfly's built in support for ACLs](https://www.dragonflydb.io/docs/managing-dragonfly/acl) with
Dragonfly Cloud.

Each Dragonfly Cloud data store is created with a default ACL rule that allows all commands for the default user.  
`USER default ON >pmn4p0ssrbbl ~* +@ALL`

To modify the data store ACL rules, click the data store three-dot
menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>)
and click *Acl Rules*  
An ACL Rules editor drawer will open where you can add, modify or delete ACL rules.

***Caution:*** Altering ACL rules can potentially disrupt access for current users. It is always recommended to test ACL
rules on a test data store before applying them to a production data store.

### How to rotate data store passkey

1. Modify the default ACL rule to e.g. `USER default ON >pmn4p0ssrbbl >mynewpass ~* +@ALL`
2. Verify you can now authenticate with both pmn4p0ssrbbl (old passkey) and mynewpass (new passkey)
3. Migrate all consumers to authenticate with the new passkey
4. Modify the default ACL rule to only include the new passkey e.g. `USER default ON >mynewpass ~* +@ALL`
5. Verify you can no longer authenticate with the old passkey.
6. ***Caution:*** It is always recommended to test ACL rules on a test data store before applying them to a production
   data store.

## Support Plans

See more information on support plans [here](./support-plans.md).
