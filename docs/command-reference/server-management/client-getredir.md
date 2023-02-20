---
description: Get tracking notifications redirection client ID if any
---

# CLIENT GETREDIR

## Syntax

    CLIENT GETREDIR 

**Time complexity:** O(1)

This command returns the client ID we are redirecting our
[tracking](https://redis.io/topics/client-side-caching) notifications to. We set a client
to redirect to when using `CLIENT TRACKING` to enable tracking. However in
order to avoid forcing client libraries implementations to remember the
ID notifications are redirected to, this command exists in order to improve
introspection and allow clients to check later if redirection is active
and towards which client ID.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the ID of the client we are redirecting the notifications to. The command returns `-1` if client tracking is not enabled, or `0` if client tracking is enabled but we are not redirecting the notifications to any client.
