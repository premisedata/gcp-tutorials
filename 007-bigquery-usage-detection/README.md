# BigQuery Usage Detection

This is a tutorial to set up an alerting service to notify you of your BigQuery usage and identify high-cost jobs.

Leveraging goblet for ease of deployment and recurring scheduled runs, this code launches a Cloud Function that:
- Analyzes BigQuery's `INFORMATION_SCHEMA` metadata to identify the most expensive BigQuery jobs that have finished running in the current day
- Sends a formatted Slack message summarizing the top 10 most expensive jobs in a concise table
- Generates a CSV file summarizing all above-average cost jobs, and stores this in a GCP Cloud Storage bucket

The goal of this service is to support users wanting to monitor/remediate BigQuery jobs. Ideally, this information will be used to help reduce BigQuery slots usage and/or minimize GCP costs.

## Deploy 

* run ```goblet deploy --project {PROJECT} --location {REGION}```
