---
description: "Pay for Dragonfly Cloud by credit card, or through AWS, GCP, or Azure Marketplace. Steps to subscribe, link your account, and troubleshoot."
sidebar_position: 0
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from '@site/src/components/CloudBadge/CloudBadge'

# Payment Methods
<CloudBadge/>
<PageTitle title="Payment Methods | Dragonfly Cloud" />

## Overview

Dragonfly Cloud invoices usage monthly. See [Pricing](./pricing.md) for what you are charged for.
You can pay by [credit card](#credit-card) or through an [AWS](#aws-marketplace), [GCP](#gcp-marketplace),
or [Azure](#azure-marketplace) Marketplace subscription.

Manage payment methods in Dragonfly Cloud under **Billing > Payment Methods**.

## Credit Card

On the **Payment Methods** page, select **Add credit card**. Usage is charged to the card monthly.

## Marketplace Subscriptions

:::warning
Subscribing in the marketplace does not link it to your Dragonfly Cloud account.
After you subscribe, use the link in the marketplace to open the Dragonfly Cloud login page, then sign in or create an account.
The link carries a token for your subscription, and the subscription is linked and approved when you log in from that page.
Signing in directly at dragonflydb.cloud does not link it.
:::

### Before You Begin

Your cloud user needs permission to purchase from the marketplace. If you do not have it, ask your cloud administrator.

- **AWS:** the `aws-marketplace:Subscribe` and `aws-marketplace:ViewSubscriptions` permissions.
  The `AWSMarketplaceManageSubscriptions` and `AWSMarketplaceFullAccess` managed policies include them.
- **GCP:** the Billing Account Administrator role on the billing account, which Google recommends for purchasers.
  Alternatively, a custom role with the Marketplace purchase permissions, such as `consumerprocurement.orders.place`.
  The Consumer Procurement Order Administrator role grants these at the billing account or organization level.
  To use **Manage on provider**, select a project that is linked to the billing account where you purchased the plan.
  Google documents that most products require the Consumer Procurement Entitlement Manager or Editor role on that project.
- **Azure:** permission to purchase from Microsoft Marketplace and at least Contributor access on the resource group.
  Free, MSDN, and similar Azure subscriptions cannot buy paid SaaS offers.

### AWS Marketplace

1. Open the [Dragonfly Cloud listing](https://aws.amazon.com/marketplace/pp/prodview-evf32lpo652gq) in AWS Marketplace
   and select **Subscribe**.
2. When the page shows *Your subscription is in progress*, select **Set up your account**.
3. On the Dragonfly Cloud login page, sign in with your existing account or select **Create one**.
4. Dragonfly Cloud shows *AWS Marketplace successfully added*.

The AWS listing uses usage-based pricing for memory (GB) and data transfer (GB).
See [Pricing](./pricing.md) for details.

### GCP Marketplace

1. Open the [Dragonfly Cloud listing](https://console.cloud.google.com/marketplace/product/dragonflydb-public/dragonfly-cloud)
   in Google Cloud Marketplace and select **Subscribe**.
2. When Google Cloud shows that your order request was sent, select **Go to product page**.
3. On the product page, select **Manage on provider**. This opens the Dragonfly Cloud login page.
4. On the Dragonfly Cloud login page, sign in with your existing account or select **Create one**.
5. Dragonfly Cloud shows *GCP Marketplace successfully added*.

### Azure Marketplace

1. Open the [Dragonfly Cloud listing](https://marketplace.microsoft.com/en-ie/product/dragonflydb.dragonfly_cloud)
   in Microsoft Marketplace and select **Get it now**.
2. Sign in to Azure, select the Azure subscription and resource group, accept the terms, and select **Complete purchase**.
3. Select **Configure account now** to open the Dragonfly Cloud login page.
4. On the Dragonfly Cloud login page, sign in with your existing account or select **Create one**.

## Linking a Marketplace Account

### Existing Customers

If you already have a Dragonfly Cloud account:

1. Go to **Billing > Payment Methods**.
2. Select **AWS Marketplace**, **GCP Marketplace**, or **Azure Marketplace**.
   Dragonfly Cloud opens the marketplace listing.
3. Follow the steps for your cloud above, and sign in with your existing Dragonfly Cloud account when prompted.

### Verify the Link

Open **Billing > Payment Methods** in Dragonfly Cloud. The marketplace subscription is listed as a payment method,
for example *GCP Marketplace Subscription*.

### Resume an Unfinished Setup

If you subscribed but did not log in to Dragonfly Cloud from the marketplace, the subscription is not linked yet.
Open the subscription in your cloud console and use its setup link:

- **AWS:** AWS Marketplace > **Manage subscriptions**, select the Dragonfly Cloud subscription,
  then select **Set up your account**.
- **GCP:** Google Cloud Marketplace > **Your orders**, open the Dragonfly Cloud product,
  then select **Manage on provider**.
- **Azure:** **SaaS** in the Azure portal, select the Dragonfly Cloud subscription,
  then use the link to the publisher's site on the subscription page.
  Azure deletes a SaaS subscription that is not configured within 30 days.

## Cancel a Marketplace Subscription

Cancel in your cloud console, not in Dragonfly Cloud. Before you cancel, add a [credit card](#credit-card)
so Dragonfly Cloud usage stays covered, and [contact support](../support.md) if you have active data stores.

- **AWS:** **Manage subscriptions**, set **Delivery method** to SaaS, select the subscription,
  then **Agreement > Actions > Cancel subscription**.
  Cancelling stops future charges. It does not refund invoices already issued, and you still owe usage already incurred.
- **GCP:** **Your orders**, select the billing account and the Dragonfly Cloud product,
  then open **Actions available to manage your orders** and select **Cancel purchase** or **Cancel subscription**.
- **Azure:** **SaaS** in the Azure portal, select the subscription, then **Cancel subscription**.
  This needs Owner or Contributor access. Cancelling removes access. Azure refunds a purchase cancelled within 72 hours,
  but not consumption billed after the account is configured.

## Troubleshooting

| Problem | What to do |
|---|---|
| You subscribed, but the marketplace is not listed under **Payment Methods**, or usage is not billed through it. | You did not log in from the marketplace page, or you logged in directly at dragonflydb.cloud. [Resume the setup](#resume-an-unfinished-setup) and log in from the page it opens. |
| You cannot find the product after subscribing. | Open your subscriptions in the cloud console, as described in [Resume an unfinished setup](#resume-an-unfinished-setup). |
| You cannot subscribe, or the subscribe button is unavailable. | Check the permissions in [Before you begin](#before-you-begin), or ask your cloud administrator. |
| The marketplace was linked to the wrong Dragonfly Cloud organization. | [Contact support](../support.md) with the organization name. |
