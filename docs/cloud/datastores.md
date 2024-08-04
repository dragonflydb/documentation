---
sidebar_position: 2
---

# Data Stores

A Dragonfly Cloud data store represents a Redis Protocol (RESP) endpoint.

To create a data store, on the *Data Stores* tab, click [+Data Store](https://dragonflydb.cloud/datastores/new)

The minimum configuration consists of *name*, *cloud provider*, *cloud region* and *plan*.

The following cloud providers are supported:
- AWS
- GCP
- Azure (Private beta, please [schedule a meeting with a product expert](https://calendly.com/d/ymz-yhv-q8f/dragonfly-cloud?month=2024-07) to get access.)

Note that the *cloud provider* and *region* can not be modified once the data store is created.

The *plan* specifies the provisioned memory and memory to CPU ratio of the data store.  
The *Enhanced* plan has more CPU for the same amount of provisioned memory and achieves higher throughput compared to the *Standard* plan.



You can modify the data store *plan* later with zero down time to scale it up or down.

By default the data store will be configured with a *public endpoint*, *TLS* and an auto generated *passkey*, meaning you can securely connect to it from anywhere over the public internet.  
To create a data store with a *private endpoint*, see [Security](#security), [Networks](./networks.md) and [Peering Connections](./connections.md).

By default the data store will consist of a single Dragonfly server, to create a highly available data store see [High Availability](#high-availability).
For cluster mode please see [Cluster Mode](#cluster-mode).

Once the data store is created, clicking the data store row will open a drawer with the data store configuration, including the auto generated passkey and a redis compatible *connection URI*. 

Once the data store *Status* becomes *Active* you can try access it with e.g. `redis-cli -u <connection URI> PING`
For more information on how to connect to the data store see [Connecting to Data Store](#connecting-to-data-store).

To update the data store configuration click the pencil edit button in the top right of the drawer.  
Dragonfly cloud performs data store updates with zero downtime.    

## Security 
Dragonfly Cloud supports public and private endpoints

### Public Endpoint 
With a public endpoint you can connect to the data store from anywhere over the internet. 
To protect your data store from unauthorized access public endpoints are configured with *passkey* and *TLS* enabled.   
*TLS* has some performance impact so can be disabled but it is highly recommended to leave it enabled.  
*Passkey* is mandatory and can not be disabled for public endpoints 

### Private Endpoint 
*Private endpoint* provides better security, performance and lower latency as the data transports to and from the data stores over private networks and not via the public internet.  
Using a private endpoint also reduces data transfer costs applied by the cloud provider.

In order to create a data store with a private endpoint, you must first create a private network, see [Networks](./networks) for more information.
Once you have created a private network, you can select it in the *Endpoint* dropdown box when creating a data store.

> ***Tip:*** In order to completely avoid data transfer charges, place your data store in the same availability zone of your application. See [High Availability](#high-availability) for specifying the data store availability zone.

*TLS* and *passkey* are disabled by default for private endpoint datastores, but can be enabled.

   
## Durability and High Availability  
### Eviction Policy 
Eviction policy controls the behavior of the datastore when it maxes out its memory.  
**No Eviction** - Items are never evicted and out of memory errors are returned when the data store is full.  
**Cache** - The data store behaves as cache and evicts items to free space for new ones when the data store is full.

### High Availability

By default the data store will consist of a single Dragonfly server, this means that in case of software failures, hardware failures or cloud zone outages data is lost and the data store may be completely unavailable.

To increase availability of your data store you can configure it to be deployed in up to three different zones, one primary zone for the master and up to two replica zones.
Dragonfly Cloud automatically detects failures and performs failover to an available replica.
Select up to three zones in the *High Availability* dropdown box.  The data store master node will be placed in the primary availability zone selected first.  
To avoid data transfer costs incurred by the cloud provider, select the primary availability zone to match the availability zone of your application. 


## Specializations

**BullMQ** - Enable this for running BullMQ workloads, this requires you to apply Redis Cluster curly braces syntax for the queue names as described [here](/docs/integrations/bullmq.md).

If that is not possible please contact support.

## Cluster Mode

By default a dragonfly cloud data store support redis cluster protocol and clients so you can seamlessly migrate from redis cluster. 

Multi node cluster is in private beta, please [schedule a meeting with a product expert](https://calendly.com/d/ymz-yhv-q8f/dragonfly-cloud?month=2024-07) to get access. 

## Connecting to Data Store

Once a data store *Status* is *Active* you can connect to it with any Redis client using the *Connection URI* provided in the data store drawer (e.g. rediss://default:h6blm92XXXsa@52tyg3xkp.dragonflydb.cloud:6385). 
Here are a few popular examples:

### Redis CLI
1. Install redis-cli, `sudo apt install redis-tools`
2. With the *Connection URI* from the data store drawer execute redis-cli in the terminal e.g. `redis-cli -u <connection URI> PING`

### Node.js
1. Install the redis npm package, `npm install redis`
2. Use the following code snippet to connect to the data store
```javascript
import { createClient } from 'redis';
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




## Support

At any time click the chat icon in the bottom right corner to ask anything, really, anything! 



