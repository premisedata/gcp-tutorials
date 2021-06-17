# Github Findings to SCC

Create/Reopen/Resolve findings from [Github Security](https://docs.github.com/en/code-security) and forward to [GCP Security Command Center](https://cloud.google.com/security-command-center)

* repository_vulnerability_alert
* code_scanning_alert
* secret_scanning_alert

## Written Tutorial

[Tutorial](https://engineering.premise.com/tutorial-publishing-github-findings-to-security-command-center-2d1749f530bc)

## Install

* pip install goblet-gcp

## Prerequisites 

* GCP Account with Security Command Center enabled
* Custom Security Command Center Source
* Github Account with at least one repo with security scanning enabled
* Python environment (>3.7) 
* Gcloud cli 

## Setup

* Set the following varibles in `.goblet/config.json`

    * "ORGANIZATION"
    * "SOURCE"
    * "GITHUB_SECRET"
    * "SERVICE_ACCOUNT_EMAIL" 

## Deploy 

* run ```goblet deploy --project=PROJECT --location LOCATION```
* Use the generated cloudfunction url and GITHUB_SECRET to create Github webhook
