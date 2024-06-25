---
sidebar_position: 5
--- 


# Monitoring
Dragonfly Cloud provides data stores observability through a readily available Grafana based [public dashboard](#public-dashboard), and a [Prometheus compatible metrics endpoint](#prometheus-compatible-metrics-endpoint) that you can scrape and integrate with most monitoring and alerts solutions like Datadog and Grafana. 

If you didn't create a datastore yet, you see [Datastores](/docs/cloud/datastores) to create your first datastore.

## Public Dashboard

To open a datastore’s public dashboard click the dashboard icon [TODO ask for help adding the icon it is available here https://fonts.google.com/icons?selected=Material+Symbols+Outlined:monitoring:FILL@1;wght@400;GRAD@0;opsz@24&icon.query=monitoring&icon.size=24&icon.color=%23e8eaed ]  

## Prometheus Compatible Metrics Endpoint

In order to access the metrics endpoint you first must acquire an API key:
1. Navigate to the Account > Keys tab.
2. Click the +Key button to open the Create Key dialog.
3. In the Create Key dialog enter a meaningful name for the key (e.g. metrics) and leave `read:metrics` selected in the permissions dropdown.
4. Click Create. The dialog will show the created key.
5. Click Copy API Key to copy the key to the clipboard.
6. Paste and store the key somewhere for later usage, Dragonfly Cloud doesn’t store the key (you can create more keys if needed).

The metrics endpoint is available for scraping at https://api.dragonflydb.cloud/v1/metrics

You can test as follows:
```bash
KEY=dragonflydb_eyJpI…MyMDYifQ==
curl https://api.dragonflydb.cloud/v1/metrics -H "authorization: Bearer $KEY”
```
Finally, configure your monitoring system with the metrics endpoint and your key.


