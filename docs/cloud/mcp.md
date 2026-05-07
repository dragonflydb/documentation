---
sidebar_position: 14
description: Manage Dragonfly Cloud from Claude, Cursor, and other LLM clients with the Dragonfly Cloud MCP server. List datastores, inspect metrics, run RESP commands, and create resources in natural language.
---

import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# MCP Server

<CloudBadge/>

## Overview

The Dragonfly Cloud MCP server exposes your account over the [Model Context Protocol](https://modelcontextprotocol.io) — an open standard for connecting LLM clients to external systems. Once configured, an MCP-aware client like Claude, Cursor, or Continue can manage your Dragonfly Cloud account in natural language: list and provision datastores, inspect metrics and slow logs, run RESP commands against a datastore, and review usage and audit history.

The server is hosted at:

```
https://api.dragonflydb.cloud/v1/mcp
```

It speaks streamable HTTP MCP and is authenticated with an MCP-scoped API key issued from the Dragonfly Cloud console. No agent install or local proxy is required.

## Prerequisites

- A Dragonfly Cloud account.
- An MCP-aware client. Common choices:
  - [Claude Code](https://docs.claude.com/en/docs/claude-code) (CLI)
  - [Claude Desktop](https://claude.ai/download)
  - [Cursor](https://cursor.com)
  - Any client that supports HTTP-transport MCP servers.

## Getting Started

### 1. Create an MCP API Key

1. Open the [API Keys](https://dragonflydb.cloud/account/keys) page in the Dragonfly Cloud console (**Account → Access → API Keys**).
2. Click **Create Key** and choose the **MCP** key type.
3. Copy the key — it begins with `dragonflydb_`. You will not be able to view it again after closing the dialog.

The MCP key is scoped to MCP usage and is independent from API keys used by the [Terraform provider](./terraform-provider.md) or other automation.

### 2. Add the Server to Your Client

Most MCP clients read a JSON configuration file. The server entry has the same shape across clients:

```json
{
  "mcpServers": {
    "dragonfly-cloud": {
      "type": "http",
      "url": "https://api.dragonflydb.cloud/v1/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_MCP_KEY>"
      }
    }
  }
}
```

Where this entry goes depends on the client:

- **Claude Code** — add to `.mcp.json` at the root of your project, or to `~/.claude.json` for global access. Claude Code prompts for approval the first time it sees a new project-scoped server.
- **Claude Desktop** — add to `claude_desktop_config.json` (location: `~/Library/Application Support/Claude/` on macOS, `%APPDATA%\Claude\` on Windows). Restart the Claude Desktop app.
- **Cursor** — add to `~/.cursor/mcp.json`.

Treat the API key as a secret: do not commit configuration files containing it to source control.

### 3. Verify the Connection

Ask your client to list your datastores. For example:

> List the datastores in my Dragonfly Cloud account.

The client should call the `list_datastores` tool and return your existing datastores. If you receive an authentication error, re-check that the `Authorization` header uses `Bearer ` followed by the full key.

## Capabilities

The server exposes tools across these areas:

- **Datastore management** — list, show, create, and delete datastores; populate a datastore with sample data.
- **Datastore inspection** — INFO output, instant Prometheus metrics, time-series CPU and memory usage, slow log entries, object histograms, and arbitrary RESP command execution.
- **Network management** — list, show, create, and delete private networks and VPC peering connections.
- **Account** — list invoices and query the account audit log.

## Example Interactions

The MCP server is designed to be used in plain language. A few prompts that work today:

- *"Create a 3 GB development datastore in `gcp/us-central1` and give me the connection string."*
- *"Show me the slow log for `prod-cache` from the last hour and group the entries by command."*
- *"What are the top memory-using key types in `prod-cache`?"* (resolved via `DEBUG OBJHIST` plus targeted `SCAN`).
- *"Create a private network in `aws/us-east-1` with CIDR `10.20.0.0/16` and peer it to my VPC `vpc-0123abcd` in account `123456789012`."*
- *"List my invoices for the last three months."*

## Security

- API keys are scoped per organization. Rotate or revoke a key from the [API Keys](https://dragonflydb.cloud/account/keys) page if it is exposed.
- All server actions are recorded in the [audit log](https://dragonflydb.cloud/account/audit-log) under the identity of the key that issued them. Use a dedicated MCP key per user or per integration so audit entries are attributable.
- The server is reachable over HTTPS only.

## Additional Resources

- [Model Context Protocol specification](https://modelcontextprotocol.io)
- [Dragonfly Cloud Console](https://dragonflydb.cloud)
- [Terraform Provider](./terraform-provider.md) — for declarative infrastructure-as-code rather than conversational management.
