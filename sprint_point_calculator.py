# Import Modules 
import requests
from requests.auth import HTTPBasicAuth
import json
import markdown
import datetime
from jira import JIRA
import sys

def getCreds (auth_file):
	with open(auth_file,'r') as af:
		gotCreds = json.loads(af.read())
		return gotCreds


# Define variables from credentials file
creds = getCreds("credentials.json")

key = creds["key"]
instance = creds["instance"]
keyOwner = creds["keyOwner"]
ignored = creds["ignore"]

# Get arguments passed to script. The main argument is the project key.
args = sys.argv

# Get the project key from args or assign a default if it wasn't passed in
if len(args) < 2:
	project = "ICS"
else:
	project = args[1]
	
## Define where to find some custom fields so we can reference them more easily in the script
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

# Iterate through all the issues and add to the list. (Jira can only return 100 issues per query.)
startAt = 0
stop = False
issues = []
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
def calculate_average_points_per_person(issues, ignored):
    points_by_person = {}
    unique_sprints_by_person = {}

    for issue in issues:
        sprints = issue['fields']['customfield_10010']
        assignee = issue['fields']['assignee']

        if not assignee:
            continue

        display_name = assignee['displayName']

        # Skip if display_name is in the ignored list
        if display_name in ignored:
            continue

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

average_points_by_person = calculate_average_points_per_person(issues, ignored)

# Sort names alphabetically
sorted_names = sorted(average_points_by_person.keys())

for name in sorted_names:
    avg_points = average_points_by_person[name]
    # Round average points to the nearest integer
    rounded_avg_points = round(avg_points)
    print(f"{name}, {rounded_avg_points} pts")
