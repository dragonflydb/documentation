---
sidebar_position: 5
---

# Append Only Mode (AOF)

At this time, Dragonfly does not support Append Only Mode (AOF). The primary reason is that the current implementation of the RDB snapshotting mechanism is not compatible with the AOF mode. The AOF mode requires a different approach to snapshotting and recovery, which is not implemented in Dragonfly, however, it is something we are considering for future versions. Please join the discussion on the [Dragonfly Discord](https://discord.com/invite/HsPjXGVH85) if you have any thoughts or suggestions on this topic.
