from goblet import Goblet, Response
from google.cloud import securitycenter
from google.cloud.securitycenter_v1 import CreateFindingRequest, Finding, SetFindingStateRequest
from hashlib import sha1, md5 
from hmac import HMAC, compare_digest
import datetime
import os 

app = Goblet(function_name="github-to-scc", local="local")

ORGANIZATION = os.environ.get("ORGANIZATION")
SOURCE = os.environ.get("SOURCE")
GITHUB_SECRET = os.environ.get("GITHUB_SECRET")

RESOLVE_ACTIONS = [
	'dismiss',
	'resolve',
	'fixed',
	'resolved',
	'closed_by_user'
]
POST_ACTIONS = [
	'create',
	'created',
	'appeared_in_branch'
]

REOPEN_ACTIONS =[
	'reopened_by_user',
	'reopened'
]

# github alerts https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#secret_scanning_alert

def extract_category(github_alert):
	if github_alert.get("instances"):
		return "CODE_SCANNING"
	if github_alert.get("affected_range"):
		return "DEPENDECY_VULNERABILITY"
	if github_alert.get("secret_type"):
		return "SECRET_SCANNING"

def remove_null(alert):
	return {k:v for k,v in alert.items() if v != None}

def verify_signature(req):
     received_sign = req.headers.get('X-Hub-Signature').split('sha1=')[-1].strip()
     secret = GITHUB_SECRET.encode()
     expected_sign = HMAC(key=secret, msg=req.data, digestmod=sha1).hexdigest()
     return compare_digest(received_sign, expected_sign)

def post_finding(client, github_event, hashed_id):
	event_time = datetime.datetime.now()
	category = extract_category(github_event["alert"])

	finding = Finding(
		state=Finding.State.ACTIVE,
		resource_name=github_event['repository']["full_name"],
		severity=Finding.Severity.SEVERITY_UNSPECIFIED,
		category=category,
		event_time=event_time,
		source_properties=remove_null(github_event['alert']),
		external_uri = github_event["repository"]["html_url"] + '/security'
	)
	request = CreateFindingRequest(
		parent=f"organizations/{ORGANIZATION}/sources/{SOURCE}",
		finding_id=hashed_id,
		finding=finding,
	)
	
	return client.create_finding(
		request=request
	)	

def set_finding_state(client, state, hashed_id):
	start_time = datetime.datetime.now()

	request = SetFindingStateRequest(
		name=f"organizations/{ORGANIZATION}/sources/{SOURCE}/findings/{hashed_id}",
		state=state,
		start_time=start_time
	)
	return client.set_finding_state(request=request)

@app.http()
def github_webhook(request):
	if not verify_signature(request):
		return Response('Forbidden',status_code=400)
	github_event = request.json
	client = securitycenter.SecurityCenterClient()

	category = extract_category(github_event["alert"])
	finding_id = github_event["alert"].get("id") or github_event["alert"].get("number")
	if not finding_id:
		return Response('Not a valid Event', status_code=501)
	full_id = f"{github_event['repository']['full_name']}{category}{finding_id}"
	hashed_id = md5(full_id.encode()).hexdigest()

	if github_event["action"] in 'create':
		post_finding(client, github_event, hashed_id)

	if github_event["action"] in RESOLVE_ACTIONS:
		set_finding_state(client, Finding.State.INACTIVE, hashed_id)

	if github_event["action"] in REOPEN_ACTIONS:
		set_finding_state(client, Finding.State.ACTIVE, hashed_id)

	return 'SUCCESS'
