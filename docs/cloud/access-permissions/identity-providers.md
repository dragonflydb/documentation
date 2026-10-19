---
description: "Configure a Microsoft Entra ID application in Azure and connect it to Dragonfly Cloud as an identity provider."
sidebar_position: 4
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Identity Providers
<CloudBadge/>
<PageTitle title="Identity Providers | Dragonfly Cloud" />

## Introduction

Connect Microsoft Entra ID to Dragonfly Cloud by registering an application in Azure and adding it as an identity provider.
Configure the Azure application first, then use its tenant and client IDs to create the provider in Dragonfly Cloud.

## Configure Azure

1. In the [Azure portal](https://portal.azure.com/), search for **App registrations** and click **New registration**.
2. Enter a descriptive **Name** and set **Supported account types** to **Accounts in this organizational directory only (Single tenant)**.
   Click **Register**.
3. Navigate to **Expose an API** in the application's left sidebar and enable the **Application ID URI**.
   Keep the default URI assigned by Azure. Copy and store this value to use when setting the scope of your token.
4. Navigate to **Manifest** in the left sidebar and change `requestedAccessTokenVersion` from `null` to `2`.
   This configures the application to use Microsoft's version 2 access tokens, the JSON Web Token (JWT) format expected by Dragonfly Cloud.
   Click **Save**.
5. In the Azure portal, go to **Enterprise applications** and select the application.
   Check that the required users have access to the application.
6. Return to the app registration and navigate to **Overview** in the left sidebar.
   Under **Essentials**, copy the **Directory (tenant) ID** and **Application (client) ID**.
   You will use these values when configuring Dragonfly Cloud.

## Configure Dragonfly Cloud

1. Navigate to **Access > Identity providers** in Dragonfly Cloud.
2. Click **+ Identity Provider**.
3. Enter a meaningful name for the provider, along with the **Directory (tenant) ID** and **Application (client) ID** copied from Azure.
4. Submit the form to create the identity provider.
