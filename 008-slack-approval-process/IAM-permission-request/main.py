import os
import json
from goblet import Goblet, goblet_entrypoint
from google.cloud import secretmanager
from slack_sdk import WebhookClient, errors

app = Goblet(function_name="IAM-permission-request")
goblet_entrypoint(app)


@app.http()
def send_iam_request(request):
    """ Parses the request and sends a message to #Infrastructure-iam-approvals
    """
    json_data = app.current_request.json
    app.log.info(f"Request: {json_data}")
    # extract data from request
    project = json_data["project"]
    resource_type = json_data["resource_type"]
    resource_name = json_data["resource_name"]
    role = json_data["role"]
    principal = json_data["principal"]
    region = json_data.get("region", "")
    user_email = json_data["user_email"]
    # get webhook from secret manager
    secret_client = secretmanager.SecretManagerServiceClient()
    webhook = secret_client.access_secret_version(
        request={"name": os.environ.get("WEBHOOK_SECRET_ID")}
    ).payload.data.decode("UTF-8")
    slack_client = WebhookClient(webhook)
    # send message
    try:
        response = slack_client.send(
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
			        },
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
                        "text": f"Requester: {user_email}"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Approve",
                            },
                            "style": "primary",
                            "action_id": "request_approve",
                            "value": f"{project},{resource_type},{resource_name},{principal},{role},{region},{user_email}",
                            "confirm": {
                                "title": {
                                    "type": "plain_text",
                                    "text": "Are you sure?",
                                },
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"{role} would be added to {principal} for {resource_name} in {project}",
                                },
                                "confirm": {"type": "plain_text", "text": "Do it"},
                                "deny": {
                                    "type": "plain_text",
                                    "text": "Stop, I've changed my mind!",
                                },
                            },
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Reject",
                            },
                            "value": f"{project},{resource_type},{resource_name},{principal},{role},{region},{user_email}",
                            "style": "danger",
                            "action_id": "request_reject",
                        },
                    ],
                },
            ],
        )
        app.log.info(response.status_code)
    except errors.SlackApiError as e:
        app.log.error(e)
