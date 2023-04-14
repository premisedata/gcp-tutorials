# GCP tutorials

The repo contains the source code for GCP tutorials written by Premise.

Please clone and star this repo to stay up to date on changes.

## Packages by Premise

[Goblet](https://github.com/goblet/goblet): An easy-to-use framework that enables developers to quickly spin up fully featured REST APIs with python on GCP

[Goblet Workflows](https://github.com/goblet/goblet_workflows): A wrapper around GCP Workflows, which is a fully-managed orchestration platform that executes services in an order that you define: a workflow. These workflows can combine services including custom services hosted on Cloud Run or Cloud Functions, Google Cloud services such as Cloud Vision AI and BigQuery, and any HTTP-based API.

[Slack Approvals](https://github.com/premisedata/slack-approval): This python library serves as the basis for managing and deploying a lightweight approval workflow based on Slack and GCP. This library contains two key classes, SlackRequest and SlackProvision as well as the logic to deploy them to GCP (See 008 for tutorial).

[Goblet GCP Client](https://github.com/goblet/goblet_gcp_client): Goblet GCP Client is a util library with support for creating GCP resource clients, GCP integration tests, and other related utils.


## Tutorials
**001 - Forward Github Security Findings to Security Command Center** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/001-github-to-scc)] [ [Written](https://engineering.premise.com/tutorial-publishing-github-findings-to-security-command-center-2d1749f530bc)] - This tutorial goes over implementation on how to automatically forward Github security findings to GCP's security command center.

**002 - Using Cloud Custodian Metric Filters to safely find and remove cloud resources** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/002-cloud-custodian-metric-filters)] [ [Written](https://engineering.premise.com/cleaning-up-your-google-cloud-environment-safety-guaranteed-2de51fb8620a)] - Learn how to combine GCP's powerful built in metrics with Cloud Custodian to easily discover potential security risks, evaluate the impact those resources currently have in your environment, and then safely address those issues. 

**003 - Setup Daily Cost Alerts on your Daily GCP Spend** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/003-cost-alerts)] [[Written](https://engineering.premise.com/tutorial-cost-spike-alerting-for-google-cloud-platform-gcp-46fd26ae3f6a)] - Deploy a cloudfunction that checks your daily GCP spend for any large cost increases or decreases in a service and notifies a slack channel

**004 - Create Dynamic Serverless Loadbalancers** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/004-dynamic-serverless-loadbalancer)] [[Written](https://austennovis.medium.com/e15751853312)] - A simple, scalable, and customizable solution to deploy and maintain  load balancers for any number of serverless applications.

**005 - Bucket Replication** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/005-bucket-replication)] [Written](https://engineering.premise.com/tutorial-bucket-replication-for-google-cloud-platform-gcp-cloud-storage-44622c59299c)] - A simple way to set up bucket replication, leveraging goblet's use of decorators to set up cloud function triggers.

**006 - Service Account Key Rotater** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/006-service-account-key-rotater)] [[Written](https://engineering.premise.com/tutorial-rotating-service-account-keys-using-secret-manager-5f4dc7142d4b)] - A pluginable solution to automate Service Account Key rotations that currently supports Github Secrets and Cloud Storage.

**007 - BigQuery Usage Detection** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/007-bigquery-usage-detection)] [Written](https://engineering.premise.com/tutorial-detection-of-high-usage-bigquery-jobs-on-google-cloud-platform-gcp-aadb591eefe5)] - A cloud function to retrieve processing info about your BigQuery jobs, send a Slack message to inform of most expensive jobs, and upload a detailed summary to a Cloud Storage bucket.

**008 - Slack Approval Process** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/008-slack-approval-process)] [Written](https://engineering.premise.com/tutorial-setting-up-approval-processes-with-slack-apps-d325aee31763)] - A quick walk-through on setting up an approval process facilitated by slack.

**009 - Cloudrun Cloudbuild Configs** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/009-cloudrun-cloudbuild-configs)] [[ Written ](https://engineering.premise.com/traffic-revisions-and-artifact-registries-in-google-cloud-run-made-easy-with-goblet-1a3fa86de25c)] - A quick walk-through on configuring cloudrun builds with goblet, including traffic, secrets, and artifact registries.

**010 - Cloudrun Jobs** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/010-cloudrun-jobs)] [[ Written ](https://medium.com/engineering-at-premise/tutorial-deploying-cloud-run-jobs-9435466b26f5)] - A tutorial on how to deploy cloudrun jobs using goblet.

**011 - Cloudrun Cors Anywhere** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/011-cloud-run-cors-anywhere)] [[ Written ](https://engineering.premise.com/tutorial-handling-cors-in-backstage-api-swagger-documentation-hosted-on-cloud-run-gcp-65584811ec0d)] - A tutorial on how to deploy cors-anywhere proxy on Cloud Run.

**012 - Backend Alerts** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/011-backend-alerts)] [[ Written ](https://engineering.premise.com/gcp-alerts-the-easy-way-alerting-for-cloudfunctions-and-cloudrun-using-goblet-62bdf2126ef6)] - A tutorial on how to deploy backend alerts alongside your codebase using goblet.

**013 - BigQuery Remote Functions** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/013-bigquery-remote-functions)] [[ Written ](https://engineering.premise.com/tutorial-deploying-bigquery-remote-functions-9040316d9d3e)] - A tutorial on how to deploy BigQuery Remote Functions on GCP using goblet.

**014 - Private Service Access using Goblet** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/014-goblet-private-services)] [[ Written ](https://engineering.premise.com/tutorial-connecting-cloudrun-and-cloudfunctions-to-redis-and-other-private-services-using-goblet-5782f80da6a0)] - A tutorial on how on deploying and connecting to private GCP services using Goblet

**015 - CloudTasks with Goblet** [[ Source ](https://github.com/premisedata/gcp-tutorials/tree/main/015-goblet-cloudtask)] [[ Written ](https://engineering.premise.com/)] - A tutorial on how to deploy CloudTaskQueues, enqueue CloudTasks and handle CloudTasks all with Goblet.
