# Backend Alerts

This is a tutorial on how to deploy a BigQuery remote functions.

## Written Tutorial

[Tutorial]()

## Install

* pip install goblet-gcp

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7 or above

## Config

You have to have a dataset created in BigQuery. In this case Dataset is called example-data-set

## Deploy

Run `goblet deploy --project {PROJECT} --location {REGION}` to deploy your application.

## Cleanup

Run `goblet destroy --project {PROJECT} --location {REGION}` to cleanup your application.
