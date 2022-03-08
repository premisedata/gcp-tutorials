# Slack approval process

A quick tutorial for setting up a Slack App for handling approval requests

The service currently supports changing IAM policies at the project level and resource level for:
* gcs buckets
* secret manager secrets
* pubsub topics and subscriptions
* bigquery tables
* cloud functions
* cloud run
* artifact registry

## Written Tutorial

[Tutorial]()

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7

## Setup

It will probably be easiest to follow the medium article, because it has screenshots and snippets.
To run through the steps briefly:
* Create slack app
* Create webhooks for the app
* Create secrets in GCP to store the webhooks
* Create service accounts that can modify iam policies for the resources you want
* Update the config files with all the variables you created above
* Deploy the cloud functions
* Update your slack app interactivity url to the endpoint for your provision function

## Deploy

Deploy by running `goblet deploy --project {PROJECT} --location {REGION}` for both the provision and request functions
