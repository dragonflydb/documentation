---
description: Learn how to use Redis CONFIG GET command to retrieve configuration parameters.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG GET

<PageTitle title="Redis CONFIG GET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `CONFIG GET` command in Redis is used to retrieve the current configuration parameters of the Redis server. This can be useful for monitoring, debugging, or auditing the server settings. Typical scenarios include checking the values of configurations like `maxmemory`, `timeout`, and `loglevel`.

## Syntax

```plaintext
CONFIG GET parameter
```

## Parameter Explanations

- **parameter**: The specific configuration setting you want to retrieve. You can use an exact parameter name (e.g., `maxmemory`) or a pattern with wildcards (e.g., `*memory*`).

## Return Values

The command returns an array of key-value pairs representing the current configuration settings that match the given parameter.

Example:

For `CONFIG GET maxmemory`, it might return:

```plaintext
1) "maxmemory"
2) "0"
```

For `CONFIG GET *memory*`, it might return:

```plaintext
1) "maxmemory"
2) "0"
3) "maxmemory-samples"
4) "5"
```

## Code Examples

```cli
dragonfly> CONFIG GET maxmemory
1) "maxmemory"
2) "0"
dragonfly> CONFIG GET *memory*
1) "maxmemory"
2) "0"
3) "maxmemory-policy"
4) "noeviction"
5) "maxmemory-samples"
6) "5"
```

## Best Practices

- Use specific parameters rather than patterns when possible to reduce the overhead on the server.
- Regularly monitor critical configurations like `maxmemory` to ensure they align with your performance and storage requirements.

## Common Mistakes

- Using overly broad patterns might retrieve more data than necessary, causing unnecessary load on the server.
- Forgetting that some configuration changes might require a server restart to take effect.

## FAQs

### What happens if I use a non-existent parameter?

The command will return an empty array if no matching configuration settings are found.

### Can I use CONFIG GET to monitor runtime changes?

Yes, `CONFIG GET` can be run at any time to check the current values of the configuration parameters, making it useful for monitoring changes in real-time.
