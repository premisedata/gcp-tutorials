# Backend Alerts

This is a tutorial on how to deploy a cloudfunction as well as various GCP monitoring alerts.

## Written Tutorial

[Tutorial](https://engineering.premise.com/gcp-alerts-the-easy-way-alerting-for-cloudfunctions-and-cloudrun-using-goblet-62bdf2126ef6)

## Install

* pip install goblet-gcp

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7 or above

## Config

Enter a Notification Channel in `config.json` if you would like the alert to trigger a channel. Otherwise you can remove the alerting section.

## Deploy

Run `goblet deploy --project {PROJECT} --location {REGION}` to deploy your application.

## Cleanup

Run `goblet destroy --project {PROJECT} --location {REGION}` to cleanup your application.
