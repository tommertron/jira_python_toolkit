import requests
from requests.auth import HTTPBasicAuth
import json
from jira import JIRA

def getCreds (auth_file):
	with open(auth_file,'r') as af:
		gotCreds = json.loads(af.read())
		return gotCreds

creds = getCreds("credentials.json")
key = creds["key"]
instance = creds["instance"]
keyOwner = creds["keyOwner"]

def getSettings():
	with open('settings.json','r') as af:
		settings = json.loads(af.read())
		return settings

def issue_getter(jql,fields):
	stop = False
	startAt = 0
	issues = []
	while stop == False:
		url = f"https://{instance}/rest/api/3/search"
		auth = HTTPBasicAuth(keyOwner, key)
		headers = {
		   "Accept": "application/json",
		   "Content-Type": "application/json"
		}
		query = {
			'jql': jql,
			'fields': fields,
			'maxResults': 100,
			"startAt": startAt
		}
		response = requests.request(
		   "GET",
		   url,
		   headers=headers,
		   params=query,
		   auth=auth
		)
		issue_seg = json.loads(response.text)
		total = issue_seg['total']
		issues += issue_seg['issues']
		if total - startAt > 100:
			startAt += 100
		else:
			stop = True
	return issues