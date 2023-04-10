# Blog Post
[link]

or 

# TL;DR
```shell
$ export GOBLET_PROJECT="goblet-cloudtask"
$ export GOBLET_LOCATION="us-central1"
$ export MY_GCP_ACCOUNT=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`
##### set the project
$ gcloud config set project $GOBLET_PROJECT
##### enable APIs
$ gcloud services enable run.googleapis.com
$ gcloud services enable cloudfunctions.googleapis.com
$ gcloud services enable cloudbuild.googleapis.com
$ gcloud services enable iam.googleapis.com 
$ gcloud services enable artifactregistry.googleapis.com
$ gcloud services enable cloudresourcemanager.googleapis.com
$ gcloud services enable apigateway.googleapis.com
$ gcloud services enable cloudtasks.googleapis.com
##### service account to run goblet deploy
$ gcloud iam service-accounts create deployer --display-name="deployer"     
$ gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/apigateway.admin"
$ gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.serviceAgent"
$ gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/run.serviceAgent"
$ gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.developer"
$ gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/run.developer"
$ gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/cloudtasks.queueAdmin"
##### service account to authenticate the CloudTask against CloudRun
$ gcloud iam service-accounts create cloudtask --display-name="cloudtask"
$ gcloud projects add-iam-policy-binding goblet-cloudtask \
  --member="serviceAccount:cloudtask@${GOBLET_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
##### service account to run the CloudRun Revision
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
##### impersonate deployer service account
$ gcloud iam service-accounts add-iam-policy-binding \
  deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com \
  --member="user:${MY_GCP_ACCOUNT}" \
  --role="roles/iam.serviceAccountTokenCreator"
$ gcloud auth application-default login \
  --impersonate-service-account=deployer@${GOBLET_PROJECT}.iam.gserviceaccount.com
##### fetch example and deploy
$ git clone https://github.com/premisedata/gcp-tutorial
$ cd gcp-tutoriales/015-goblet-cloudtask
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ goblet deploy -l $GOBLET_LOCATION -p $GOBLET_PROJECT
# test
$ SERVICE_URL=`gcloud run services list \
  --filter=SERVICE:cloudtask-example --format="value(URL)"
$ curl $SERVICE_URL/enqueue \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```