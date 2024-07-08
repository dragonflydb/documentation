---
description: Learn how to use Redis ROLE command to retrieve the role of the server.
---

import PageTitle from '@site/src/components/PageTitle';

# ROLE

<PageTitle title="Redis ROLE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ROLE` command in Redis is used to provide information about the role of the instance in a replication setup. It is particularly useful for understanding whether a Redis server is operating as a master, slave, or sentinel. Typical scenarios for using this command include monitoring replication status, debugging replication issues, and ensuring high availability configurations.

## Syntax

```plaintext
ROLE
```

## Parameter Explanations

The `ROLE` command does not require any parameters.

## Return Values

The return structure of the `ROLE` command varies depending on the role of the Redis instance:

- **Master:**

  ```plaintext
  1) "master"
  2) (integer) number_of_slaves
  3) 1) "slave_ip"
     2) "slave_port"
     3) "slave_state"
  ```

  Example:

  ```plaintext
  1) "master"
  2) (integer) 2
  3) 1) 1) "127.0.0.1"
        2) "6379"
        3) "online"
     2) 1) "127.0.0.1"
        2) "6380"
        3) "online"
  ```

- **Slave:**

  ```plaintext
  1) "slave"
  2) "master_ip"
  3) (integer) master_port
  4) "replication_state"
  5) (integer) data_received_offset
  ```

  Example:

  ```plaintext
  1) "slave"
  2) "127.0.0.1"
  3) (integer) 6379
  4) "connected"
  5) (integer) 12345
  ```

- **Sentinel:**
  ```plaintext
  1) "sentinel"
  2) 1) "monitored_master_name_1"
     2) "monitored_master_name_2"
  ```
  Example:
  ```plaintext
  1) "sentinel"
  2) 1) "mymaster"
     2) "yourmaster"
  ```

## Code Examples

```cli
dragonfly> ROLE
1) "master"
2) (integer) 1
3) 1) 1) "127.0.0.1"
      2) "6380"
      3) "online"

dragonfly> ROLE
1) "slave"
2) "127.0.0.1"
3) (integer) 6379
4) "connected"
5) (integer) 45678

dragonfly> ROLE
1) "sentinel"
2) 1) "mymaster"
     2) "anothermaster"
```

## Best Practices

- Regularly use the `ROLE` command to monitor the state of your Redis instances, especially in complex replication setups.
- Automate checks of the `ROLE` output to trigger alerts for unexpected role changes or issues in replication.

## Common Mistakes

- Ignoring the `ROLE` output format: Ensure that scripts parsing the `ROLE` output correctly handle its different formats for master, slave, and sentinel roles.

## FAQs

### What happens if I run the `ROLE` command on a standalone Redis instance?

For a standalone instance with no replication configured, the `ROLE` command will still indicate "master" as its role.

### Can the `ROLE` command be used to check the status of network connections between masters and slaves?

Yes, the `ROLE` command provides information about the connection status of slaves to the master, which can be useful for detecting network issues.
