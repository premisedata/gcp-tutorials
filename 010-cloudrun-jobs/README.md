# Cloud Run Jobs

This is a tutorial on how to deploy a cloudrun job using goblet.

## Written Tutorial

[Tutorial]()

## Install

* pip install goblet-gcp

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7 or above

## Config

Enter service account in `config.json` if you are deploying a scheduled job

## Deploy

Run `goblet deploy --project {PROJECT} --location {REGION}` to deploy your application.

## Cleanup

Run `goblet destroy --project {PROJECT} --location {REGION}` to cleanup your application.
