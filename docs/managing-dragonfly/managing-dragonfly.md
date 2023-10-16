---
sidebar_position: 5
---

# Managing Dragonfly

### Limits

Listed below are known Dragonfly limitations.

* Each Dragonfly instance can handle up to two billion keys
* Lists, Sets and Hashes can contain up to two billion values
* The expire limit for keys is `2^28` seconds, so around 8 years
* Each command can contain up to `2^16` arguments
* Each argument can be up to 256MB bytes long
* String values are limited to a size of 256MB