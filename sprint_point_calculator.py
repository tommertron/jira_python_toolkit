# Import Modules 
import requests
from requests.auth import HTTPBasicAuth
import json
import markdown
import datetime
from jira import JIRA

# commit test

def getCreds (auth_file):
	with open(auth_file,'r') as af:
		gotCreds = json.loads(af.read())
		return gotCreds


# Define variables from credentials file
creds = getCreds("credentials.json")

key = creds["key"]
assignee = creds["assignee"]
instance = creds["instance"]
keyOwner = creds["keyOwner"]
destinationFile = creds["destinationFile"]

# Define Project Key
project = "FBIC"
spoints = 'customfield_10061' #name of the field in your jira instance that holds story points
sprint = 'customfield_10010'

# Jira Query Function
def get_issues(startAt):
	url = f"https://{instance}/rest/api/3/search"
	auth = HTTPBasicAuth(keyOwner, key)
	headers = {
	   "Accept": "application/json",
	   "Content-Type": "application/json"
	}

	query = {
		'jql': f'project = {project} AND Sprint in closedSprints() AND status = "Done" ORDER BY resolutiondate',
 		'fields': f'issuetype,summary,status, {spoints}, {sprint}, assignee',
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
	return response

# Convert data to workable data in the script
startAt = 0
stop = False
issues = []

# Iterate through all the issues and add to the list. (Jira can only return 100 issues per query.)
while stop == False:
	results = get_issues(startAt)
	jdata = json.loads(results.text)
	total = jdata['total']
	issues = issues + jdata['issues']
	if total - startAt > 100:
		startAt += 100
	else:
		stop = True

## Make the average points by person function 
def calculate_average_points_per_person(issues):
    points_by_person = {}
    unique_sprints_by_person = {}

    for issue in issues:
        sprints = issue['fields']['customfield_10010']
        assignee = issue['fields']['assignee']

        if not assignee:
            continue

        display_name = assignee['displayName']
        story_points = issue['fields']['customfield_10061']

        if story_points is None:
            continue

        closed_sprints = [sprint for sprint in sprints if sprint['state'] == 'closed']

        if closed_sprints:
            if display_name not in points_by_person:
                points_by_person[display_name] = story_points
                unique_sprints_by_person[display_name] = set([sprint['id'] for sprint in closed_sprints])
            else:
                points_by_person[display_name] += story_points
                unique_sprints_by_person[display_name].update([sprint['id'] for sprint in closed_sprints])

    average_points_by_person = {}
    for name in points_by_person:
        unique_sprints_count = len(unique_sprints_by_person[name])
        average_points_by_person[name] = points_by_person[name] / unique_sprints_count

    return average_points_by_person


average_points_by_person = calculate_average_points_per_person(issues)

for name, avg_points in average_points_by_person.items():
    print(f"{name}, {avg_points:.2f} pts")
