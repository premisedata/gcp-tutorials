import certifi
import ssl
import os
from slack_sdk import WebClient
# slack webhook
ssl_context = ssl.create_default_context(cafile=certifi.where())
slack_client = WebClient(token=os.environ.get(
    "SLACK_BOT_TOKEN"), ssl=ssl_context)
slack_channel_id = os.environ.get("SLACK_CHANNEL_ID")


def send_slack_message(app, project_id, services):
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"GCP Services Low Usage Alert - Project: {project_id}", "emoji": True,},
        },
        {
            "type": "divider",
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "The following services are under the threshold:",
            },
        },
    ]

    fields = []
    counter = 0
    for service in services:
        field = {
            "type": "mrkdwn",
            "text": f"> *Service*: {service['name']}",
        }
        if 'cpu' in service:
            field["text"] += f"\n> *CPU*: {service['cpu']}%"
        if 'memory' in service:
            field["text"] += f"\n> *Memory*: {service['memory']}%"
        fields.append(field)

        counter += 1
        # if the counter is divisible by 10, create a new block
        if counter % 10 == 0:
            blocks.append({
                "type": "section",
                "fields": fields
            })

            # reset the fields list
            fields = []
    
    # append the final block (if there are any remaining fields)
    if fields:
        blocks.append({
            "type": "section",
            "fields": fields
        })

    app.log.debug(f"Sending slack message: {blocks}")

    slack_client.chat_postMessage(
        channel=slack_channel_id, text="fallback", blocks=blocks,
    )
