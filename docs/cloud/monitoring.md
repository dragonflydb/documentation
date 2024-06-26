---
sidebar_position: 5
---

# Monitoring

Dragonfly Cloud provides data stores observability through a readily available Grafana based [public dashboard](#public-dashboard), and a [Prometheus compatible metrics endpoint](#prometheus-compatible-metrics-endpoint) that you can scrape and integrate with most monitoring and alerts solutions like Datadog and Grafana.

If you didn't create a datastore yet, you see [Datastores](/docs/cloud/datastores) to create your first datastore.

## Public Dashboard


To open a datastore’s public dashboard click the dashboard icon (<svg style={{marginBottom: "-3px", marginLeft: "3px"}} xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="white"><path d="M120-120v-80l80-80v160h-80Zm160 0v-240l80-80v320h-80Zm160 0v-320l80 81v239h-80Zm160 0v-239l80-80v319h-80Zm160 0v-400l80-80v480h-80ZM120-327v-113l280-280 160 160 280-280v113L560-447 400-607 120-327Z"/></svg>) in the relevant datastore row.  
A Grafana based dashboard will open in a new tab.


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
