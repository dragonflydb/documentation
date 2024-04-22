---
sidebar_position: 3
---

# Append Only File (AOF)

Append Only File (AOF) captures every write operation received by the server.
Upon server restart, these operations can be replayed to reconstruct the original dataset.
The commands are logged in the same format that adheres to the Redis protocol.

**Currently, Dragonfly does not support AOF.**
The primary reason is the lack of high-priority demand within the community.
Implementing AOF in Dragonfly would require a different approach than in Redis and is more sophisticated, especially in terms of maintaining high performance.
However, we are exploring the possibility of including this feature in future releases.
If you have any thoughts or suggestions about this, we encourage you to join the conversation on our [Discord server](https://discord.com/invite/HsPjXGVH85).
