---
sidebar_position: 10
---

# Known Limitations

Listed below are known Dragonfly limitations:

* Each Dragonfly instance can handle up to two billion keys.
* Lists, Sets and Hashes can contain up to two billion values.
* The expiration limit for keys is `2^28` seconds, which is around 8 years.
* Each command can contain up to `2^16` arguments (can be changed with the `max_multi_bulk_len` flag).
* Each argument can be up to 256MB bytes long.
* String values are limited to a size of 256MB.