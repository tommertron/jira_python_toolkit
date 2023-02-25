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
	'jql': f'project = {project} AND Sprint in openSprints() and assignee = "{assignee}"',
	'fields': 'issuetype,summary,status, estimate',
	'maxResults': 100,
	"startAt": 0 #Remember to do this a few times to get all the data!
}
response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth
)

# Convert data to workable data in the script 
qdata = (json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
jdata = json.loads(qdata)

issueList = 'key,issuetype,Final Estimate,Initial Estimate,Current Estimate,status'

json_data = qdata
def generate_issue_list (data, output_file):

    headers = ['To do', 'In progress', 'Monitoring', 'Blocked', 'Done']
    statuses = {'To do': [], 'In progress': [], 'Monitoring': [], 'Blocked': [], 'Done': []}

    # sort issues into appropriate status list
    for issue in data['issues']:
        if issue['fields']['status']['name'] == 'To Do':
            statuses['To do'].append(issue)
        elif issue['fields']['status']['name'] == 'In Progress':
            statuses['In progress'].append(issue)
        elif issue['fields']['status']['name'] == 'Monitoring':
            statuses['Monitoring'].append(issue)
        elif issue['fields']['status']['name'] == 'Blocked':
            statuses['Blocked'].append(issue)
        elif issue['fields']['status']['name'] == 'Done':
            statuses['Done'].append(issue)

    with open(output_file, 'w') as f:
        # write header for each status list
        for header in headers:
            issues = statuses[header]
            if issues:
                f.write(f"## {header}\n")
                for issue in issues:
                    # format each issue
                    key = issue['key']
                    summary = issue['fields']['summary']
                    url = f"https://corusbss.atlassian.net/browse/{key}"
                    f.write(f"- [{summary}]({url})\n")
                f.write("\n")

#write_issues_to_file('/Users/tomrobertson/Library/CloudStorage/OneDrive-CorusEntertainmentInc/Obsidian/Work/Sprint Items.md',jdata, )
generate_issue_list(jdata, destinationFile)
