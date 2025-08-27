---
sidebar_position: 6
---

import PageTitle from '@site/src/components/PageTitle';

# Network Bandwidth

<PageTitle title="Network Bandwidth | Dragonfly Cloud" />

## Overview

For heavy network traffic workloads, please refer to the following tables to understand the network bandwidth available for each data store size and compute tier in various cloud providers.
If you have more customized network bandwidth requirements, please contact support.

## Amazon Web Services (AWS)

- AWS provides burstable network bandwidth for certain data store sizes.
- Burst bandwidth can be used for short periods of time but is not guaranteed.

| Compute Tier | Size (GB) | Bandwidth (Gbps)    | Burst Bandwidth (Gbps)  |
|--------------|-----------|---------------------|-------------------------|
| Dev          | 3         | 0.256               | 5.0                     |
| Standard     | 12.5      | 0.5                 | 10.0                    |
| Standard     | 25        | 0.75                | 10.0                    |
| Standard     | 50        | 1.25                | 10.0                    |
| Standard     | 100       | 2.5                 | 10.0                    |
| Standard     | 200       | 5                   | 10.0                    |
| Standard     | 400       | 12                  | -                       |
| Enhanced     | 6.5       | 0.5                 | 10.0                    |
| Enhanced     | 12.5      | 0.75                | 10.0                    |
| Enhanced     | 25        | 1.25                | 10.0                    |
| Enhanced     | 50        | 2.5                 | 10.0                    |
| Enhanced     | 100       | 5                   | 10.0                    |
| Enhanced     | 200       | 12                  | -                       |
| Enhanced     | 300       | 20                  | -                       |
| Enhanced     | 400       | 25                  | -                       |
| Extreme      | 6.25      | 0.75                | 10.0                    |
| Extreme      | 12.5      | 1.25                | 10.0                    |
| Extreme      | 25        | 2.5                 | 10.0                    |
| Extreme      | 50        | 12                  | -                       |
| Extreme      | 100       | 20                  | -                       |
| Extreme      | 200       | 25                  | -                       |

## Google Cloud Platform (GCP)

| Compute Tier | Size (GB) | Bandwidth (Gbps)  |
|--------------|-----------|-------------------|
| Dev          | 3         | 1.0               | 
| Standard     | 12.5      | 10.0              |
| Standard     | 25        | 10.0              |
| Standard     | 50        | 16.0              |
| Standard     | 100       | 32.0              |
| Standard     | 200       | 32.0              |
| Standard     | 400       | 32.0              |
| Enhanced     | 6.5       | 10.0              |
| Enhanced     | 12.5      | 10.0              |
| Enhanced     | 25        | 16.0              |
| Enhanced     | 50        | 32.0              |
| Enhanced     | 100       | 32.0              |
| Enhanced     | 200       | 32.0              |
| Enhanced     | 300       | 32.0              |
| Enhanced     | 400       | 32.0              |
| Extreme      | 6.25      | 10.0              | 
| Extreme      | 12.5      | 16.0              |
| Extreme      | 25        | 32.0              |
| Extreme      | 50        | 32.0              | 
| Extreme      | 100       | 32.0              | 
| Extreme      | 200       | 32.0              |
