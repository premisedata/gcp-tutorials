# Private Service Access using Goblet

This is a tutorial for connecting to a Redis instance using an Internal IP leveraging GCP Cloud Run and VPC Connector.

## Written Tutorial 
[Tutorial]()

## Install

* pip install goblet-gcp

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7 or above

## Config

For Redis configuration, specify PROJECT in authorizedNetwork in `config.json`.

For VPC Connector configuration update ipCidrRange in `config.json` if necessary, default is 10.32.1.0/28

## Deploy

Run `goblet deploy --project {PROJECT} --location {REGION}` to deploy your application.

## Cleanup

Run `goblet destroy --project {PROJECT} --location {REGION}` to cleanup your application.