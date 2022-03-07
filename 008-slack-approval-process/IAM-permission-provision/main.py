import os
import json
from goblet import Goblet, goblet_entrypoint, Response
from slack_sdk.signature import SignatureVerifier
from slack_sdk import WebhookClient, errors
from google.cloud import secretmanager

app = Goblet(function_name="IAM-permission-provision")
goblet_entrypoint(app)


@app.http()
def provision_iam_request(request):
    """Main method
    """
    # get slack signature secret from secret manager
    secret_client = secretmanager.SecretManagerServiceClient()
    signing_secret = secret_client.access_secret_version(
        request={"name": os.environ.get("SIGNATURE_SECRET_ID")}
    ).payload.data.decode("UTF-8")
    # validate request using the signature secret
    if not is_valid_signature(
        request.headers, request.get_data(as_text=True), signing_secret
    ):
        return Response("Forbidden", status_code=403)
    # parse the slack action
    payload = json.loads(request.form["payload"])
    action = payload["actions"][0]
    action_id = action["action_id"]
    action_value = action["value"]
    user = ' '.join(payload["user"]["name"].split('.'))
    project, resource_type, resource_name, principal, role, region, user_email = action_value.split(",")
    # get slack webhooks from secret manager
    secret_client = secretmanager.SecretManagerServiceClient()
    webhook = secret_client.access_secret_version(
        request={"name": os.environ.get("WEBHOOK_SECRET_ID")}
    ).payload.data.decode("UTF-8")
    # Sends to the status slack channel open to the whole company
    status_slack_client = WebhookClient(webhook)
    # Edits the original message to show that it has been responded to
    response_url = payload["response_url"]
    response_slack_client = WebhookClient(response_url)
    if action_id == "request_approve":
        try:
            if resource_type == "bucket":
                add_bucket_iam_access(project, resource_name, role, principal)
            elif resource_type == "secret":
                add_secret_iam_access(project, resource_name, role, principal)
            elif resource_type == "topic":
                add_topic_iam_access(project, resource_name, role, principal)
            elif resource_type == "subscription":
                add_subscription_iam_access(project, resource_name, role, principal)
            elif resource_type == "bq-table":
                add_bq_table_iam_access(project, resource_name, role, principal)
            elif resource_type == "function":
                add_function_iam_access(project, resource_name, role, principal, region)
            elif resource_type == "cloud-run":
                add_run_iam_access(project, resource_name, role, principal, region)
            elif resource_type == "registry":
                add_artifact_registry_iam_access(project, resource_name, role, principal, region)
            elif resource_type == "project":
                add_project_iam_access(project, role, principal)
            else:
                app.log.error(f"Unsupported resource: {resource_type}")
                send_status_message(
                    status_slack_client, project, resource_type, resource_name, role, principal, region, user_email, "Resource not supported"
                )
                return
        except Exception as e:
            app.log.error(f"Error while provisioning: {e}")
            for client in (status_slack_client, response_slack_client):
                send_status_message(
                    client, project, resource_type, resource_name, role, principal, region, user_email, f"Error while provisioning: {e}"
                )
            return Response("Error while provisioning", status_code=400)
        app.log.info(f"Added {principal} with {role} to {resource_name} in {project}")
        app.log.info("Sending approved status message")
        for client in (status_slack_client, response_slack_client):
            send_status_message(
                client, project, resource_type, resource_name, role, principal, region, user_email, f"Approved by {user}"
            )
    elif action_id == "request_reject":
        app.log.info("Sending rejected status message")
        for client in (status_slack_client, response_slack_client):
            send_status_message(
                client, project, resource_type, resource_name, role, principal, region, user_email, f"Rejected by {user}"
            )


def is_valid_signature(headers, data, signing_secret):
    """Validates the request from the Slack integration
    """
    timestamp = headers["x-slack-request-timestamp"]
    signature = headers["x-slack-signature"]
    verifier = SignatureVerifier(signing_secret)
    return verifier.is_valid(data, timestamp, signature)


def send_status_message(client, project, resource_type, resource_name, role, principal, region, user_email, status):
    """Sends request status message through the provided slack client
    """
    try:
        response = client.send(
            text="fallback",
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "IAM Request",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "text": {
				        "type": "mrkdwn",
				        "text": f"Project: {project}"
			        },
                },
                {
                    "type": "section",
                    "text": {
				        "type": "mrkdwn",
                        "text": f"Resource Type: {resource_type}"
                    }
                },
                {
                    "type": "section",
                    "text": {
				        "type": "mrkdwn",
				        "text": f"Resource Name: {resource_name if not region else region + '/' + resource_name}"
			        },
                },
                {
                    "type": "section",
                    "text": {
				        "type": "mrkdwn",
				        "text": f"Role: {role}"
			        },
                },
                {
                    "type": "section",
                    "text": {
				        "type": "mrkdwn",
				        "text": f"Principal: {principal}"
			        },
                },
                {
                    "type": "section",
                    "text": {
				        "type": "mrkdwn",
				        "text": f"Status: {status}"
			        },
                },
                {
                    "type": "section",
                    "text": {
				        "type": "mrkdwn",
				        "text": f"Requester: {user_email}"
			        },
                },
            ],
        )
        app.log.info(response.status_code)
    except errors.SlackApiError as e:
        app.log.error(e)
    

def add_binding(client, resource, role, principal):
    """Generic add-binding procedure
    Not every resource has this method available though. Need to check to the docs
    """
    policy = client.get_iam_policy(request={"resource": resource})
    policy.bindings.add(role=role, members=[principal])
    client.set_iam_policy(request={"resource": resource, "policy": policy})


def add_bucket_iam_access(project, bucket_name, role, principal):
    """Adds bucket access for the principal
    """
    from google.cloud import storage

    storage_client = storage.Client(project)
    bucket = storage_client.bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": role, "members": {principal}})
    bucket.set_iam_policy(policy)


def add_secret_iam_access(project, secret_name, role, principal):
    """Adds secret access for the principal
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project}/secrets/{secret_name}"
    add_binding(client, secret_path, role, principal)


def add_topic_iam_access(project, topic_name, role, principal):
    """Adds topic access for the principal
    """
    from google.cloud import pubsub_v1

    client = pubsub_v1.PublisherClient()
    topic_path = f"projects/{project}/topics/{topic_name}"
    add_binding(client, topic_path, role, principal)


def add_subscription_iam_access(project, subscription_name, role, principal):
    """Adds subscription access for the principal
    """
    from google.cloud import pubsub_v1

    client = pubsub_v1.SubscriberClient()
    subscription_path = f"projects/{project}/subscriptions/{subscription_name}"
    add_binding(client, subscription_path, role, principal)


def add_bq_table_iam_access(project, table_name, role, principal):
    """Adds table access for the principal

    :param table_name: {table's dataset}.{table name}
    """
    from google.cloud import bigquery

    client = bigquery.Client()
    name = f"{project}.{table_name}"
    table = client.get_table(name)
    policy = client.get_iam_policy(table)
    policy.bindings.append({"role": role, "members": {principal}})
    client.set_iam_policy(table, policy)


def add_function_iam_access(project, function_name, role, principal, region):
    """Adds function access for the principal
    """
    from google.cloud import functions_v1

    client = functions_v1.CloudFunctionsServiceClient()
    function_path = f"projects/{project}/locations/{region}/functions/{function_name}"
    add_binding(client, function_path, role, principal)


def add_run_iam_access(project, service_name, role, principal, region):
    """Adds cloud run service access for the principal
    """
    from googleapiclient import discovery
    from oauth2client.client import GoogleCredentials

    credentials = GoogleCredentials.get_application_default()
    client = discovery.build("run", "v1", credentials=credentials).projects().locations().services()
    from google.iam.v1.policy_pb2 import Policy
    resource = f"projects/{project}/locations/{region}/services/{service_name}"
    policy = client.getIamPolicy(resource=resource).execute()
    bindings = policy.get("bindings", [])
    bindings.append({"role": f"{role}", "members": [f"{principal}"]})
    policy["bindings"] = bindings
    response = client.setIamPolicy(resource=resource, body={"policy": policy}).execute()


def add_project_iam_access(project, role, principal):
    """
    """
    from google.cloud import resourcemanager_v3

    client = resourcemanager_v3.ProjectsClient()
    project_path = f"projects/{project}"
    add_binding(client, project_path, role, principal)


def add_artifact_registry_iam_access(project, registry_name, role, principal, region):
    """
    """
    from google.cloud import artifactregistry_v1beta2

    client = artifactregistry_v1beta2.ArtifactRegistryClient()
    registry_path = f"projects/{project}/locations/{region}/repositories/{registry_name}"
    add_binding(client, registry_path, role, principal)

