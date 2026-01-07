---
sidebar_position: 4
---

# Install Dragonfly using Linux Packages

Dragonfly provides native packages for RPM-based and Debian-based Linux distributions. These packages are hosted at [packages.dragonflydb.io](https://packages.dragonflydb.io/) and are signed with GPG keys for security.

## RPM-Based Distributions

For Fedora, RHEL, CentOS, and other RPM-based distributions, you can install Dragonfly using the YUM/DNF package manager.

### Add the Repository

Add the Dragonfly repository to your system:

```shell
sudo dnf config-manager addrepo --from-repofile=https://packages.dragonflydb.io/dragonfly.repo
```

### Install Dragonfly

Install Dragonfly:

```shell
sudo dnf install -y dragonfly
```

## Debian/Ubuntu-Based Distributions

For Debian, Ubuntu, and other APT-based distributions, you can install Dragonfly using the APT package manager.

### Add the GPG Key

Download and add the Dragonfly GPG public key:

```shell
sudo curl -Lo /usr/share/keyrings/dragonfly-keyring.public https://packages.dragonflydb.io/pgp-key.public
```

### Add the Repository

Add the Dragonfly repository sources:

```shell
sudo curl -Lo /etc/apt/sources.list.d/dragonfly.sources https://packages.dragonflydb.io/dragonfly.sources
```

### Install Dragonfly

Update the package list and install Dragonfly:

```shell
sudo apt update && sudo apt install -y dragonfly
```

## Start Dragonfly

Start the Dragonfly service:

```shell
sudo systemctl start dragonfly
```

To make Dragonfly start automatically when your system boots:

```shell
sudo systemctl enable dragonfly
```

You can combine both commands into one:

```shell
sudo systemctl enable --now dragonfly
```

## Verify Installation

Check that the Dragonfly service is running:

```shell
sudo systemctl status dragonfly
```

You should see output indicating the service is "active (running)".

You can also connect to the running instance using `redis-cli`:

```shell
redis-cli -p 6379 PING
```

You should see a `PONG` response if Dragonfly is running correctly.

## Version Availability

The YUM/DNF repository maintains the latest 5 releases, allowing you to install specific versions as needed. The APT repository contains the latest version of Dragonfly. If you need an older version on Debian/Ubuntu systems, you can download the package directly from the [GitHub releases page](https://github.com/dragonflydb/dragonfly/releases).

## Next Steps

- Learn about [configuring Dragonfly](../managing-dragonfly/flags.md)
- Set up [replication](../managing-dragonfly/replication.md) for high availability
- Configure [backups](../managing-dragonfly/backups.md)
