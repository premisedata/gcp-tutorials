# Bucket Replication

A quick tutorial for setting up bucket replication

We leverage goblet's use of decorators to set up triggers for Cloud Functions, to treat the service like one Cloud Function with multiple triggers.

## Written Tutorial

[Tutorial]()

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7

## Setup

Make sure you have a service account with `storage.objectViewer` for the source bucket and `storage.objectAdmin` for the destination bucket.
It is probably best to set this up at the bucket level.

Replace all the placeholders in `.goblet/config.json` and `bucket_replications.json` with your project, service account, and bucket pairings.

## Deploy

Deploy by running `goblet deploy --project {PROJECT} --location {REGION}`
