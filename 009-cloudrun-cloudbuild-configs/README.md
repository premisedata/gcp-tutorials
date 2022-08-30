# Cloud Run and Cloud Build Configurations

This is a quick tutorial on how to set traffic and other configurations for Cloud Run deployments.

Configurations shown:
* cloudrun
* cloudrun_revision
* cloudrun_container
* cloudbuild

## Written Tutorial

[Tutorial](https://engineering.premise.com/traffic-revisions-and-artifact-registries-in-google-cloud-run-made-easy-with-goblet-1a3fa86de25c)

## Install

* pip install goblet-gcp

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7 or above

## Traffic

Enter desired traffic in the `cloudrun` key. It can be any integer from 0 to 100. 

## Artifact Registry

If using an external artifact registry, pass it through the `cloudbuild` key. Cross-project artifact registries will require a service account with permissions for the external artifact registry as well.

## Environment Variables and Secrets

Pass in evironment variables through the `cloudbuild_container` key. Secrets can also be passed in as environment variables but will require an additional service account with permissions to each secret which can be passed in through the `cloudrun_revision` key.

## Additional Configurations

In addition to the configurations listed, you can pass in any other field for [cloudrun_revision](https://cloud.google.com/run/docs/reference/rest/v2/projects.locations.services#RevisionTemplate), [cloudrun_container](https://cloud.google.com/run/docs/reference/rest/v2/Container), and [cloudrun_container](https://cloud.google.com/build/docs/api/reference/rest/v1/projects.builds#Build).

## Deploy

Run `goblet deploy --project {PROJECT} --location {REGION}` to deploy your application.
