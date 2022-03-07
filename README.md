# GCP tutorials

The repo contains the source code for GCP tutorials written by Premise.

Please clone and star this repo to stay up to date on changes.

## Packages by Premise

[Goblet](https://github.com/anovis/goblet): An easy-to-use framework that enables developers to quickly spin up fully featured REST APIs with python on GCP

## Tutorials
**001 - Forward Github Security Findings to Security Command Center** [[ Source ](https://github.com/premisedata/gcp-tutorials/001-github-to-scc)] [ [Written](https://engineering.premise.com/tutorial-publishing-github-findings-to-security-command-center-2d1749f530bc)] - This tutorial goes over implementation on how to automatically forward Github security findings to GCP's security command center.

**002 - Using Cloud Custodian Metric Filters to safely find and remove cloud resources** [[ Source ](https://github.com/premisedata/gcp-tutorials/002-cloud-custodian-metric-filters)] [ [Written](https://engineering.premise.com/cleaning-up-your-google-cloud-environment-safety-guaranteed-2de51fb8620a)] - Learn how to combine GCP's powerful built in metrics with Cloud Custodian to easily discover potential security risks, evaluate the impact those resources currently have in your environment, and then safely address those issues. 

**003 - Setup Daily Cost Alerts on your Daily GCP Spend** [[ Source ](https://github.com/premisedata/gcp-tutorials/003-cost-alerts)] [[Written](https://engineering.premise.com/tutorial-cost-spike-alerting-for-google-cloud-platform-gcp-46fd26ae3f6a)] - Deploy a cloudfunction that checks your daily GCP spend for any large cost increases or decreases in a service and notifies a slack channel

**004 - Create Dynamic Serverless Loadbalancers** [[ Source ](https://github.com/premisedata/gcp-tutorials/004-dynamic-serverless-loadbalancer)] [[Written](https://austennovis.medium.com/e15751853312)] - A simple, scalable, and customizable solution to deploy and maintain  load balancers for any number of serverless applications.

**005 - Bucket Replication** [[ Source ](https://github.com/premisedata/gcp-tutorials/005-bucket-replication)] [Written](https://engineering.premise.com/tutorial-bucket-replication-for-google-cloud-platform-gcp-cloud-storage-44622c59299c)] - A simple way to set up bucket replication, leveraging goblet's use of decorators to set up cloud function triggers.

**006 - Service Account Key Rotater** [[ Source ](https://github.com/premisedata/gcp-tutorials/006-service-account-key-rotater)] [Written]()] - A pluginable solution to automate Service Account Key rotations that currently supports Github Secrets and Cloud Storage.

**007 - BigQuery Usage Detection** [[ Source ](https://github.com/premisedata/gcp-tutorials/007-bigquery-usage-detection)] [Written]()] - A cloud function to retrieve processing info about your BigQuery jobs, send a Slack message to inform of most expensive jobs, and upload a detailed summary to a Cloud Storage bucket.

**008 - Slack Approval Process** [[ Source ](https://github.com/premisedata/gcp-tutorials/008-slack-approval-process)] [[ Written ]()] - A quick walk-through on setting up an approval process facilitated by slack.