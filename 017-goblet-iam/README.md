# Goblet IAM

A tutorial on how Goblet simplfies GCP IAM by auto generating required deployment permissions and creating a deployment service account.

## Written Tutorial

[Tutorial]()

## Install

* pip install goblet-gcp

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7 or above


## Check and Enable GCP Services

Run `goblet services check` to view all GCP services that are needed for this application.
Run `goblet services enable` to enable any required servies that are not yet enabled. 

## View Required Permissions

Run `goblet services autogen_iam`. This will create an IAM policy in `.goblet/autogen_iam_role.json`. 
In this example this will create a role with permissions to deploy a `cloudfunction`, `scheduled job` `pubsub_topic` and `pubsub subscription`. Goblet will also add invoker permissions on the `cloudfunction` for the service accounts assigned to the scheduled job and pubsub subscription. 

## Create Service Account

Run `goblet services create_service_account -p PROJECT`.
This will create a custom role and service account based on your application name.  

## Deploy

Run `goblet deploy -p PROJECT -l LOCATION`

## Cleanup

Run `goblet destroy -p PROJECT -l LOCATION`
