---
sidebar_position: 1
---

# Getting Started

There are several options available to get Dragonfly up and running quickly.

Install Dragonfly

- [Install with Docker](./docker.md)
- [Install with Docker Compose](./docker-compose.md)
- [Install Dragonfly Kubernetes Operator](./kubernetes-operator.md)
- [Install on Kubernetes with Helm Chart](./kubernetes.md)
- [Install from Binary](./binary.md)

# Hardware Compatibility
Dragonfly is specifically optimized to operate in cloud environments.
It is officially supported and certified for use on both x86_64 and arm64 architectures.

For x86_64 architectures, Dragonfly requires a minimum *sandybridge* architecture to function properly.
To ensure compatibility and performance, Dragonfly undergoes continuous testing on various cloud platforms. These include Graviton2 instances in AWS cloud, as well as x86_64 based instances in both AWS and GCP clouds.

Furthermore, Dragonfly's regression tests, which can be [found here](https://github.com/dragonflydb/dragonfly/actions/workflows/regression-tests.yml), are continously run on Azure cloud via GitHub Actions.
This helps guarantee the reliability and stability of the software.

# OS Compatibility
Dragonfly is compatible with Linux versions 4.14 or later.
However, to achieve optimal performance, it is recommended to run Dragonfly on kernel version 5.10 or later.
The Dragonfly build environment is based on Ubuntu 20.04.