---
sidebar_position: 13
---

# Terraform Provider for Dragonfly Cloud

## Overview

The Dragonfly Cloud Terraform Provider allows you to manage your Dragonfly Cloud resources using infrastructure as code. This provider is currently in beta and enables you to automate the provisioning and management of your Dragonfly Cloud infrastructure. The provider is available on both the [Terraform Registry](https://registry.terraform.io/providers/dragonflydb/dfcloud/latest) and [OpenTofu Registry](https://search.opentofu.org/provider/dragonflydb/dfcloud/latest).

## Installation

You can install the Dragonfly Cloud Terraform provider using the following methods:

### Automated Installation

Run the setup script to automatically download and install the provider into your local Terraform folder:

```bash
wget -qO- https://raw.githubusercontent.com/dragonflydb/terraform-provider-dfcloud/refs/heads/main/setup.sh | sh
```

### Manual Configuration

To use the provider in your Terraform configuration, include the following provider block:

```hcl
terraform {
  required_providers {
    dfcloud = {
      source = "registry.terraform.io/dragonflydb/dfcloud"
    }
  }
}


provider "dfcloud" {
  api_key = "<YOUR_API_KEY>"
}
```

## Authentication

The provider requires an API token for authentication. You can provide this token in one of two ways:

1. Environment variable:
```bash
export DFCLOUD_API_KEY="your_api_token"
```

2. Provider configuration (as shown in the example above)

## Available Resources

The Dragonfly Cloud Terraform provider allows you to manage various resources in your Dragonfly Cloud environment. Documentation for specific resources and their usage can be found in the provider's official documentation.

Key resource types include:
- Dragonfly Datastore Configuration
- Network configurations
- Connection configurations

## Example Usage

Here's a basic example of creating a Dragonfly instance:

```hcl
resource "dfcloud_datastore" "cache" {
  name = "frontend-cache"

  location = {
    region   = "us-central1"
    provider = "gcp"
  }
 
  tier = {
    max_memory_bytes = 3000000000
    performance_tier = "dev"
    replicas         = 1
  }

  dragonfly = {
    cache_mode = true
  }
}
```


## Additional Resources

- [Terraform Registry](https://registry.terraform.io/providers/dragonflydb/dfcloud/latest)
- [OpenTofu Registry](https://search.opentofu.org/provider/dragonflydb/dfcloud/latest)
- [Provider GitHub Repository](https://github.com/dragonflydb/terraform-provider-dfcloud)
- [Examples](https://github.com/dragonflydb/terraform-provider-dfcloud/tree/main/examples)
- [Issue Tracker](https://github.com/dragonflydb/terraform-provider-dfcloud/issues)

