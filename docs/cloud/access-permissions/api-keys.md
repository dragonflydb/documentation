---
description: "Create and manage Dragonfly Cloud API keys for programmatic access, metrics scraping, and Terraform."
sidebar_position: 3
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# API Keys
<CloudBadge/>
<PageTitle title="API Keys | Dragonfly Cloud" />

## Introduction

API keys let you access Dragonfly Cloud programmatically, without a user session.
Common uses include scraping the [Prometheus-compatible metrics endpoint](../monitoring.md#prometheus-compatible-metrics-endpoint)
and authenticating the [Terraform provider](../terraform-provider.md).

## Creating an API Key

- Navigate to the [Account > API Keys](https://dragonflydb.cloud/account/keys) tab in Dragonfly Cloud.
- Click the **+API Key** button to open the **Create Key** dialog.
- Enter a meaningful name for the key (e.g., `metrics`).
- Select the desired access level in the **Permissions** dropdown (for example, **Read Metrics**).
- Optionally, for keys with only the **Read Metrics** permission, set a **Scope** to restrict the key to tagged data stores.
  See [Scoping a Key to Tagged Data Stores](#scoping-a-key-to-tagged-data-stores).
- Click **Create**, and the dialog will show the created key.
- Click **Copy API Key** to copy the key to the clipboard.

:::warning
Dragonfly Cloud does not store the key itself. Store it somewhere secure, as it cannot be shown again.
:::

## Using an API Key

Pass the key in the `Authorization` header as a bearer token:

```bash
# Replace with your API key.
$> KEY="dragonflydb_eyJpI...fQ=="

$> curl https://api.dragonflydb.cloud/v1/metrics -H "Authorization: Bearer $KEY"
```

## Scoping a Key to Tagged Data Stores

Keys with only the **Read Metrics** permission can be scoped to a set of [data store tags](../datastores.md#tags).
A scoped key can read metrics only for data stores whose tags match **every** key/value pair in the scope.
For example, a key with the scope `env=prod` can read metrics only for data stores tagged `env=prod`.
A key without a scope can read metrics for all data stores in the account.

- Set the scope in the **Scope** field when creating the key.
- To change the scope of an existing key, open the key's menu in the
  [Account > API Keys](https://dragonflydb.cloud/account/keys) tab and select **Edit**.
  Clearing all scope entries makes the key unscoped.

## Managing and Revoking Keys

All keys in your account are listed in the [Account > API Keys](https://dragonflydb.cloud/account/keys) tab.
Delete a key there to revoke it immediately. Create a separate key per integration so each can be rotated or revoked independently.
