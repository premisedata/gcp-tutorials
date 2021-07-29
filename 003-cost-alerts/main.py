from goblet import Goblet
from slack_sdk.webhook import WebhookClient
import os 
from datetime import datetime,timezone,timedelta
import urllib.parse
from google.cloud import bigquery

app = Goblet(function_name="gcp-cost-spike-alert", local="local")

# Thresholds
AMOUNT = 250
AMOUNT_CHANGED = 500
PERCENTAGE = 1.1

# ENV Vars
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
BILLING_ORG = os.environ.get("BILLING_ORG")
BILLING_ID = os.environ.get("BILLING_ID")
BQ_TABLE = os.environ.get("BQ_TABLE")

webhook = WebhookClient(SLACK_WEBHOOK)

# Set Schedule Here
@app.schedule("0 15 * * *", timezone="EST")
def post_slack():
    daily_costs = get_daily_costs()
    flagged_costs = parse_cost_changes(daily_costs)
    for cost in flagged_costs:
        # Add Additional Integrations Here 
        webhook.send(text="fallback", blocks=slack_block(cost))

# Query to get Daily Costs
def get_daily_costs():
    client = bigquery.Client()
    now = datetime.now(timezone.utc)
    prev_utc = now -timedelta(2)
    curr_utc = now - timedelta(1)
    
    QUERY = (
        f"""SELECT
        project.name as project,
        sku.id as sku_id,
        sku.description as sku_def,
        service.id as service_id,
        service.description as service_def,
        SUM(CASE WHEN EXTRACT(DAY FROM usage_start_time) = {prev_utc.day} THEN cost ELSE 0 END) AS prev_day,
        SUM(CASE WHEN EXTRACT(DAY FROM usage_start_time) = {curr_utc.day} THEN cost ELSE 0 END) AS curr_day,
        FROM `{BQ_TABLE}`
        WHERE DATE_TRUNC(usage_start_time, DAY) = "{prev_utc.strftime('%Y-%m-%d')}" or DATE_TRUNC(usage_start_time, DAY) = "{curr_utc.strftime('%Y-%m-%d')}"
        GROUP BY 1,2,3,4,5
        ORDER BY 1;"""
    )
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()
    return rows

# Extract Large Spikes from Costs
def parse_cost_changes(rows):
    flagged_items = []
    for item in rows:
        i1 = float(item["prev_day"])
        i2 = float(item["curr_day"])
        if (i1 > AMOUNT or i2 > AMOUNT) and i1 != 0 and i2 != 0 and ((i2 /i1) >= PERCENTAGE or (i1 /i2) >= PERCENTAGE) or abs(i2-i1) >= AMOUNT_CHANGED:
            flagged_items.append(item)
    return flagged_items

# Slack Message Formatting 
def slack_block(item):
    encoded_sku = urllib.parse.quote_plus(f"services/{item['service_id']}/skus/{item['sku_id']}")
    billing_link = f"https://console.cloud.google.com/billing/{BILLING_ID}/reports;projects={item['project']};skus={encoded_sku}?organizationId={BILLING_ORG}&orgonly=true"
    
    now = datetime.now(timezone.utc)
    prev_utc = now -timedelta(2)
    curr_utc = now - timedelta(1)

    return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Large Cost Change Detected:*\n*<{billing_link}|View in Billing>*"
			}
		},
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Project:*\n{item['project']}"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*SKU:*\n{item['sku_def']}"
			}
		},
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Service:*\n{item['service_def']}"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*Previous Cost ({prev_utc.strftime('%Y-%m-%d')}):*\n${item['prev_day']:.2f}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Latest Cost ({curr_utc.strftime('%Y-%m-%d')}):*\n${item['curr_day']:.2f}"
				}
			]
		},
		{
			"type": "divider"
		}
	]
