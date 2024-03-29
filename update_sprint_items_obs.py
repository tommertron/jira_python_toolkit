# Import Modules 
import requests
from requests.auth import HTTPBasicAuth
import json
import markdown
import datetime
from jira import JIRA

def getCreds (auth_file):
	with open(auth_file,'r') as af:
		gotCreds = json.loads(af.read())
		return gotCreds

creds = getCreds("credentials.json")

key = creds["key"]
assignee = creds["assignee"]
project = creds["project"]
instance = creds["instance"]
keyOwner = creds["keyOwner"]
destinationFile = creds["destinationFile"]


# Import Issues from Jira 
url = f"https://{instance}/rest/api/3/search"
auth = HTTPBasicAuth(keyOwner, key)
headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

query = {
	'jql': f'project = {project} AND Sprint in openSprints() and assignee = "{assignee}" ORDER BY Rank ASC',
	'fields': 'issuetype,summary,status, estimate',
	'maxResults': 100,
	"startAt": 0
}
response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth
)

# Convert data to workable data in the script 
jdata = json.loads(response.text)

# Function to go through the issues and generate the list of issues for the assignee
def generate_issue_list (data):

	headers = creds["statuses"]
	statuses = {}

	# sort issues into appropriate status list
	for header in headers:
		statuses[header] = []
		for issue in data['issues']:
			if issue['fields']['status']['name'] == header:
				statuses[header].append(issue)

	for header in headers:
		issues = statuses[header]
		if issues:
			print(f"## {header}\n")
			for issue in issues:
				# format each issue
				key = issue['key']
				summary = issue['fields']['summary']
				url = f"https://{instance}/browse/{key}"
				print(f"- [{summary}]({url})")


generate_issue_list(jdata)