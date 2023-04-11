# CloudTasks and CloudTaskQueues using Goblet

This is a tutorial on how to use Goblet to create and handle [CloudTasks](https://cloud.google.com/tasks/docs).

## Written Tutorial 
[Tutorial](https://engineering.premise.com/)

## Prerequisites 

* GCP Account
* GCP CLI
* Python 3.7 or above

## Setup
### Environment Variables
```shell
export GOBLET_PROJECT="" # goblet-cloudtask
export GOBLET_LOCATION="" # us-central1
export MY_GCP_ACCOUNT=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`
# set the project
gcloud config set project $GOBLET_PROJECT
```
### Enable APIs
```shell
gcloud services enable run.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable iam.googleapis.com 
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable apigateway.googleapis.com
gcloud services enable cloudtasks.googleapis.com
```

### Create and Configure Service Accounts
```shell
# service account to deploy infrastructure and code
gcloud iam service-accounts create deployer --display-name="deployer"     
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/apigateway.admin"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.serviceAgent"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/run.serviceAgent"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.developer"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/run.developer"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/cloudtasks.queueAdmin"
  
# service account to authenticate the CloudTask against CloudRun
gcloud iam service-accounts create cloudtask --display-name="cloudtask"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:cloudtask@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

# service account to run the CloudRun Revision
gcloud iam service-accounts create cloudrun --display-name="cloudrun"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:cloudrun@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/cloudtasks.enqueuer"
gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:cloudrun@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/run.viewer"
gcloud iam service-accounts add-iam-policy-binding \
  cloudtask@${GOBLET_PROJECT}.iam.gserviceaccount.com \
  --member="serviceAccount:cloudrun@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```
### Impersonate `deployer` Service Account
```shell
##### impersonate deployer service account
gcloud iam service-accounts add-iam-policy-binding \
  deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com \
  --member="user:${MY_GCP_ACCOUNT}" \
  --role="roles/iam.serviceAccountTokenCreator"
gcloud auth application-default login \
  --impersonate-service-account=deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com
```

## Deploy
```shell
git clone https://github.com/premisedata/gcp-tutorial
cd gcp-tutoriales/015-goblet-cloudtask
sed "s/{PROJECT}/$GOBLET_PROJECT/g" .goblet/config.json.sample > .goblet/config.json

python3 -m venv venv
. venv/bin/activate
(venv) pip install -r requirements.txt
(venv) goblet deploy -l $GOBLET_LOCATION -p $GOBLET_PROJECT
```

## Test
```shell
SERVICE_URL=`gcloud run services list \
  --filter=SERVICE:cloudtask-example --format="value(URL)"
  
curl $SERVICE_URL/enqueue \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```