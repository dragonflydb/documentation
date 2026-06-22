---
description: Learn how Dragonfly Cloud BYOC keeps your data plane in your own cloud account while Dragonfly manages operations.
sidebar_position: 1
slug: /cloud/byoc
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Bring Your Own Cloud (BYOC)

<CloudBadge/>

<PageTitle title="BYOC | Dragonfly Cloud" />

## Overview

Dragonfly Cloud BYOC gives you the same managed Dragonfly Cloud experience while provisioning and operating the data plane in your own cloud account.

With BYOC:

- **Your data stays in your environment**. Dragonfly servers and backup storage run in your cloud account.
- **Dragonfly still operates the service**. The Dragonfly Cloud control plane manages provisioning, updates, and ongoing operations.
- **You retain network and compliance control**. The deployment model fits organizations that need tighter ownership over cloud resources and data residency.
- **You can use existing cloud commitments and discounts**. This can improve cost efficiency compared to fully hosted deployments.

The Dragonfly Cloud control plane runs in the Dragonfly Cloud account, while the data plane runs in your cloud account.

If you are interested in Dragonfly Cloud BYOC, please [contact us](https://www.dragonflydb.io/request-demo) to start a proof-of-concept.

## Supported Cloud Providers

Dragonfly Cloud BYOC currently supports:

- **Amazon Web Services (AWS)**
- **Google Cloud Platform (GCP)**

## Architecture

Dragonfly Cloud BYOC separates management from workload execution:

- The **control plane** stays in Dragonfly Cloud and is responsible for orchestration and service management.
- The **data plane** runs in your cloud account and includes the Dragonfly instances and backup storage.
- Each managed instance runs a **Dragonfly Cloud agent** that establishes an encrypted outbound tunnel back to the control plane.

Because the agent initiates the connection, **you do not need to allow inbound internet access** to your Dragonfly instances for routine management.

## Access Model

To let Dragonfly Cloud manage resources in your cloud account, you create a role with limited permissions and register it in the Dragonfly Cloud console.

- Dragonfly Cloud assumes this role only when it needs to provision or manage BYOC resources.
- The role follows the **principle of least privilege**.
- For AWS:
    - Access is limited to resources tagged as `managed-by: dragonfly-cloud`.
    - Role assumption is protected with a **shared secret**, so only your Dragonfly Cloud BYOC account can use it.

You can review the exact permissions in the public onboarding templates:

- AWS CloudFormation: [customer_role.yaml](https://prodv2-control-plane-byoc-public.s3.us-east-1.amazonaws.com/customer_role.yaml)
- GCP Terraform: [main.tf](https://prodv2-control-plane-byoc-public.s3.us-east-1.amazonaws.com/main.tf)

For stricter isolation, Dragonfly recommends using a **dedicated cloud account or project** for BYOC workloads.

## Security and Operations

Dragonfly Cloud BYOC is designed to keep operational access narrow and auditable.

### Control Plane Access

The Dragonfly Cloud agent on each instance provides the secure communication path back to the control plane. This connection is encrypted and initiated from your environment.

### Operations Team Access

When operational access is required, the Dragonfly Cloud agent exposes a pseudo-SSH server over the same secure tunnel. Each such session is logged for audit purposes.

### Telemetry

Each instance also runs a telemetry agent that sends metrics and logs over TLS to an authenticated endpoint in the Dragonfly Cloud control plane.

### Backups

Backups are stored in cloud storage buckets in your cloud account, so both the serving layer and the backup data remain under your cloud ownership.

## Shared Responsibility Model

In a BYOC deployment:

- **Dragonfly Cloud is responsible** for delivering the managed service, including provisioning workflows, operations, and service reliability, subject to the [Dragonfly Cloud SLA](https://www.dragonflydb.io/sla).
- **You are responsible** for maintaining the required access to your cloud account and ensuring sufficient quotas and limits for the resources that Dragonfly Cloud needs to provision.

## Creating BYOC Data Stores

The user experience for BYOC data stores is the same as for non-BYOC private endpoint deployments.

1. Create a [network](../networks.md) for your data stores.
2. Create a [data store with a private endpoint](../datastores.md#private-endpoint) in that network.
3. Connect that network to your application environment through [peering connections](../connections.md).

This keeps data traffic on private networking paths while preserving the standard Dragonfly Cloud workflow for managed deployments.

## When to Choose BYOC

BYOC is the ideal deployment model if your organization requires:

- **Strict data residency or compliance controls** that mandate all workloads remain entirely within your own cloud boundary.
- **Private networking restrictions** where VPC peering with a Dragonfly-managed cloud account is impossible.
- **Managed service experience** that allows Dragonfly to manage the software lifecycle without you relinquishing ownership of the underlying infrastructure.
- **Optimized cloud cost alignment** by leveraging your existing enterprise discounts, cloud spend commitments, or specific procurement workflows.

## Getting Started
To evaluate Dragonfly Cloud BYOC for your environment, [contact us](https://www.dragonflydb.io/request-demo) to start a proof-of-concept.
