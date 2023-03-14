# Import Modules 
import requests
from requests.auth import HTTPBasicAuth
import json
from jira import JIRA

# commit test

def getCreds (auth_file):
	with open(auth_file,'r') as af:
		gotCreds = json.loads(af.read())
		return gotCreds

# define credential stuff
creds = getCreds("credentials.json")
key = creds["key"]
instance = creds["instance"]
keyOwner = creds["keyOwner"]

# define variables
epics = creds["epics"]


# Define the query function
def querier(jql):
	url = f"https://{instance}/rest/api/3/search"
	auth = HTTPBasicAuth(keyOwner, key)
	headers = {
	   "Accept": "application/json",
	   "Content-Type": "application/json"
	}
	query = {
		'jql': jql,
		'fields': 'issuetype,summary,status',
		'maxResults': 0,
		"startAt": 0
	}
	response = requests.request(
	   "GET",
	   url,
	   headers=headers,
	   params=query,
	   auth=auth
	)
	return response

# Define the function to get issue totals
def total_getter (jql):
	result = querier(jql)
	query_result = json.loads(result.text)
	return query_result['total']
	
# Define the function to get project name
def project_name_getter():
	url = f"http://{instance}/rest/api/2/issue/{epic}"
	auth = HTTPBasicAuth(keyOwner, key)
	headers = {
	   "Accept": "application/json",
	   "Content-Type": "application/json"
	}
	response = requests.request(
	   "GET",
	   url,
	   headers=headers,
	   auth=auth
	)
	info = json.loads(response.text)
	return info["fields"]["summary"]

for epic in epics:
	# Get total number of issues
	total_issues = total_getter(f'parent = {epic}')
	# Get issues that are done
	done_issues = total_getter(f'parent = {epic} AND status = Done')
	# Get Project Name
	project_name = project_name_getter()
	percent_done = done_issues / total_issues * 100
	print (f'## [{project_name}](https://{instance}/browse/{epic})')
	print (f'*{done_issues}* issues done of *{total_issues}* total issues. (**{percent_done:.0f}% complete**)\n')