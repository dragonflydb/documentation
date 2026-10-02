---
description: "Connect MCP-compatible AI assistants and agents to your Dragonfly Cloud data stores using the hosted MCP server."
sidebar_position: 16
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# MCP
<CloudBadge/>
<PageTitle title="MCP | Dragonfly Cloud" />

## Overview

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that lets AI assistants and agents (such as GitHub Copilot, Claude, and Cursor) securely connect to external systems through a common interface. Instead of relying on static, pre-trained knowledge, an MCP-compatible client can discover and call a well-defined set of "tools" exposed by an MCP server, letting it take real, up-to-date actions against a live system on your behalf.

Dragonfly Cloud provides a hosted MCP server that exposes your Dragonfly Cloud account and data stores as tools for any MCP-compatible AI assistant or agent. Once configured, an AI agent can use these tools to inspect and manage your Dragonfly Cloud resources on your behalf.

## Security and Responsibility

MCP tools can perform **destructive, irreversible operations** on your Dragonfly Cloud account, including modifying or deleting data stores, networks, and connections, depending on the scope of the API key you provide. An AI agent will act on instructions from its underlying model, which can misinterpret a request or be manipulated by malicious or untrusted content it processes. You are responsible for how you configure and operate an MCP client against your Dragonfly Cloud account. In particular:

- **Control access.** Treat your MCP API key like any other credential. Only share it with MCP clients and agents you trust, and store it securely.
- **Apply least privilege.** Prefer the **Read-Only MCP** scope unless the agent genuinely needs to make changes. Only use **Full-Access MCP** when read/write access is required, and rotate or revoke keys that are no longer needed.
- **Review AI agent actions.** Review the tool calls an agent proposes before approving them, especially for any operation that modifies or deletes resources, and monitor your account activity afterward.
- **Scope the blast radius.** Use a dedicated API key per agent or integration rather than reusing one key everywhere, so you can revoke access independently if a specific client misbehaves or is compromised.

Dragonfly Cloud does not expose your data store credentials (such as passwords) through the MCP server by default.

## Generating an API Key

Access to the MCP server is authenticated using a Dragonfly Cloud API key with an MCP-specific scope:

- Navigate to the [Access > API Keys](https://dragonflydb.cloud/account/keys) tab in Dragonfly Cloud.
- Click the [+API Key](https://dragonflydb.cloud/account/keys) button to open the **Create Key** dialog.
- In the **Create Key** dialog, enter a meaningful name for the key (e.g., `mcp`).
- In the **Permissions** dropdown, select one of the following scopes:
  - **Full-Access MCP** — allows the agent to both read and modify your Dragonfly Cloud resources.
  - **Read-Only MCP** — allows the agent to read your Dragonfly Cloud resources, but not modify them.
- Click **Create**, and the dialog will show the created key.
- Click **Copy API Key** to copy the key to the clipboard.
- Store the key somewhere secure for later usage. Dragonfly Cloud doesn't store the key itself.

## Configuring an MCP Client

The Dragonfly Cloud MCP server is available at `https://api.dragonflydb.cloud/v1/mcp`, and is accessed over HTTP using your API key as a bearer token in the `Authorization` header.

Add the following to your MCP client's configuration, replacing `<DFCLOUD_API_KEY>` with the API key generated above:

```json
{
  "servers": {
    "dragonflycloud": {
      "url": "https://api.dragonflydb.cloud/v1/mcp",
      "headers": {
        "Authorization": "Bearer <DFCLOUD_API_KEY>"
      }
    }
  }
}
```

:::note
The exact location and format of this configuration depends on your MCP client. Consult your client's documentation for how to add a remote, HTTP-based MCP server.
:::

Once configured, restart or reload your MCP client so it picks up the new server. Your AI assistant should now be able to discover and use the tools exposed by the Dragonfly Cloud MCP server, scoped to the permissions of the API key you used.

## Detailed Client Setup

Choose your preferred AI client below and follow its setup instructions. In each case, replace the placeholder with the Full-Access or Read-Only MCP API key you generated above.

### Visual Studio Code

Add the following to your VS Code `settings.json` file (or to `.vscode/mcp.json` for a workspace-specific server):

```json
{
  "servers": {
    "dragonflycloud": {
      "url": "https://api.dragonflydb.cloud/v1/mcp",
      "headers": {
        "Authorization": "Bearer <DFCLOUD_API_KEY>"
      }
    }
  }
}
```

### Cursor

Edit your Cursor `mcp.json` configuration file (**Settings > Cursor Settings > MCP**) to add the Dragonfly Cloud MCP server:

```json
{
  "mcpServers": {
    "dragonflycloud": {
      "url": "https://api.dragonflydb.cloud/v1/mcp",
      "headers": {
        "Authorization": "Bearer <DFCLOUD_API_KEY>"
      }
    }
  }
}
```

### Claude Desktop and Claude.ai

Claude Desktop and Claude.ai support remote MCP servers through **Settings > Connectors**:

1. Open **Settings > Connectors** and click **Add custom connector**.
2. Enter a name (e.g., `Dragonfly Cloud`) and the server URL `https://api.dragonflydb.cloud/v1/mcp`.
3. When prompted for authentication, choose a header-based option and supply the header `Authorization` with the value `Bearer <DFCLOUD_API_KEY>`.
4. Save, then enable the connector in your conversation's tools list.

### Claude Code

Add the Dragonfly Cloud MCP server with a single command:

```bash
claude mcp add dragonflycloud \
  -t http https://api.dragonflydb.cloud/v1/mcp \
  -H "Authorization: Bearer <DFCLOUD_API_KEY>"
```

### Codex CLI

Edit your `~/.codex/config.toml` and include the following:

```toml
[mcp_servers.dragonflycloud]
command = "npx"
args = ["-y", "mcp-remote@latest", "https://api.dragonflydb.cloud/v1/mcp", "--header", "Authorization: Bearer <DFCLOUD_API_KEY>"]
```

### LM Studio

In LM Studio's **Program > Install > Edit mcp.json** panel, add:

```json
{
  "mcpServers": {
    "dragonflycloud": {
      "url": "https://api.dragonflydb.cloud/v1/mcp",
      "headers": {
        "Authorization": "Bearer <DFCLOUD_API_KEY>"
      }
    }
  }
}
```

### Other MCP Clients

Any MCP client that supports remote, HTTP-based servers with custom headers can connect to Dragonfly Cloud using the same two pieces of information:

- **Server URL:** `https://api.dragonflydb.cloud/v1/mcp`
- **Header:** `Authorization: Bearer <DFCLOUD_API_KEY>`

Consult your client's documentation for where to enter these values.
