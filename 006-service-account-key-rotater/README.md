# Secret Key Rotation

Rotate Service Account Keys in GCP Secret Manager.

The default age for a key is set by `KEY_VALID_DAYS` with the default `2`. They will rotated everyday, so you should get the latest everyday.

The default rotation period for a key is set by `ROTATION_PERIOD_SECONDS` with the default `86400s`, this will allow the key to be rotated on a daily basis.

To create a new key use the `service-account-key-rotater` endpoint. The request  `service_account_name` and `project`.

```{"service_account_name":"NAME", "project":"PROJECT"}```

The keys are rotated through a pubsub topic.

## Written Tutorial

[Tutorial](https://engineering.premise.com/tutorial-rotating-service-account-keys-using-secret-manager-5f4dc7142d4b)

## Getting Keys 

### Locally

Use gcloud functions call api.

```bash
gcloud functions call get-secret-key --project {PROJECT} --region {REGION} --data '{"service_account_name":"SERVICE_ACCOUNT", "project":"PROJECT"'
```

If you have jq you can pipe the results directly into a service account file

```bash
gcloud functions call get-secret-key --project {PROJECT} --region {REGION} --data '{"service_account_name":"SERVICE_ACCOUNT", "project":"PROJECT"' --format json | jq  -r '.result' | base64 --decode > "service-acount.json"
```


## Github Plugin

The organization for Github Secret Rotation is set by `GH_ORGANIZATION`.

This app will automatically update github secrets with the new keys. 
In order to use this flow, make sure to update the labels of the creation request to include `type`, this will allow you to specify `github`.

To update the secret for a given repository be sure to include the `ghr` flag which will allow you to specify the Github Repository to be updated. In order to update an Organizational level secret be sure to set `gho` to `True`.

`sn` is an optional flag that allows you to specify the Secret Name and defaults to `GCP_SA_KEY`.

Note: ghr must be lowercase and type must reflect github

```
{
    "service_account_name":"NAME", 
    "project":"PROJECT",
    "labels" : [{
        "type": "github",
        "ghr" : "deployment-dev",
        "sn": "GCP_SA_KEY"
    },{
        "type": "github",
        "gho" : True,
        "sn": "GCP_SA_KEY"
    }]
}
```


## Google Cloud Storage Plugin

The bucket for key rotation is set by `STORAGE_BUCKET_NAME`.

This application will automatacially update the designated bucket with new keys. In order to use this flow, make sure to update the labels of the creation request to include `type`, this will allow you to specify `storage`.

`sn` is an optional flag that allows you to specify the Secret Name and defaults to `GCP_SA_KEY`.

Note: type must reflect storage

```
{
    "service_account_name":"NAME", 
    "project":"PROJECT",
    "labels" : [{
        "type": "storage",
        "sn": "GCP_SA_KEY"
    }]
}
```
### Using secret mananger client

`base64.decode(client.get(name=SA_NAME))`

## Install

* pip install goblet-gcp

## Deploy 

* need to set goblet configs for `PROJECT`, `serviceAccountEmail`
* need to create service account for secret manager and give it `Service Account Key Admin` and `Secret Manager Admin` permissions
`gcloud alpha services identity create \
    --service "secretmanager.googleapis.com" \
    --project {PROJECT}`
* create pubsub topic `secret-rotation` and give the secret manager service account publish permissions
* run ```goblet deploy -p {PROJECT} -l {REGION}```