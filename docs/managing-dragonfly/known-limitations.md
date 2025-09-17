---
sidebar_position: 10
---

# Known Limitations

Listed below are known Dragonfly limitations:

* Each Dragonfly instance can handle up to two billion keys *per CPU thread*.
* Lists, Sets and Hashes can contain up to two billion values.
* TTLs are 32 bits, which roughly translates to 136 years. If a TTL higher than that,
  Dragonfly quietly rounds it down to 136 years.
* Each command can contain up to `2^16` arguments (can be changed with the `max_multi_bulk_len` flag).
* Each argument can be up to 256MB bytes long.
* String values sizes are limited to 256MB.
