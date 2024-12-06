---
sidebar_position: 5
---

# Monitoring

## Overview

Dragonfly Cloud provides observability through the following monitoring features:

- A readily available Grafana-based [public dashboard](#public-dashboard).
- A [Prometheus-compatible metrics endpoint](#prometheus-compatible-metrics-endpoint) that you can scrape and integrate with most monitoring and alerting solutions like Datadog and Grafana.

If you have not yet created a Dragonfly Cloud data store, please refer to the [getting started](getting-started.md) guide.

## Public Dashboard

- To open a data store's public dashboard, click the dashboard icon (<svg style={{marginBottom: "-3px", marginLeft: "3px"}} xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="white"><path d="M120-120v-80l80-80v160h-80Zm160 0v-240l80-80v320h-80Zm160 0v-320l80 81v239h-80Zm160 0v-239l80-80v319h-80Zm160 0v-400l80-80v480h-80ZM120-327v-113l280-280 160 160 280-280v113L560-447 400-607 120-327Z"/></svg>) in the relevant data store row.  
- A Grafana-based dashboard will open in a new tab.

## Prometheus Compatible Metrics Endpoint

### Generating an API Key

In order to access the metrics endpoint, you must first acquire an API key:

- Navigate to the [Account > API Keys](https://dragonflydb.cloud/account/keys) tab in Dragonfly Cloud.
- Click the [+API Key](https://dragonflydb.cloud/account/keys) button to open the **Create Key** dialog.
- In the **Create Key** dialog, enter a meaningful name for the key (e.g., `metrics`).
- Leave **Read Metrics** selected in the **Permissions** dropdown.
- Click **Create**, and the dialog will show the created key.
- Click **Copy API Key** to copy the key to the clipboard.
- Store the key somewhere secure for later usage. Dragonfly Cloud doesn't store the key itself.

### Accessing the Metrics Endpoint

- Once you have the API key, you can use it to access the metrics endpoint.
- The metrics endpoint is available for scraping at `https://api.dragonflydb.cloud/v1/metrics`.
- Configure your monitoring system with the metrics endpoint and your API key to start monitoring your data store.
- The API key should be passed in the `Authorization` header as a bearer token like so:

```bash
# Replace with your API key.
$> KEY="dragonflydb_eyJpI...fQ=="

# Send a request to the metrics endpoint.
$> curl https://api.dragonflydb.cloud/v1/metrics -H "Authorization: Bearer $KEY"
```
