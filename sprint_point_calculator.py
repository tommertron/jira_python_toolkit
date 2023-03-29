# Import Modules 
import requests
from requests.auth import HTTPBasicAuth
import json
import markdown
import datetime
from jira import JIRA
import sys
from toolkit_tools import issue_getter
from toolkit_tools import getSettings


# Define variables from universal settings file
settings = getSettings()
ignored = settings['ignored_people']
points = settings['points']
sprint = settings['sprint']

# Get arguments passed to script. The main argument is the project key.
args = sys.argv

# Get the project key from args or assign a default if it wasn't passed in
if len(args) < 2:
	project = "ICS"
else:
	project = args[1]

# Define query and get issues
jql = f'project = {project} AND Sprint in closedSprints() AND status = "Done" ORDER BY resolutiondate',
fields = f'issuetype,summary,status, {points}, {sprint}, assignee',
issues = issue_getter(jql,fields)

## Make the average points by person function 
def calculate_average_points_per_person(issues, ignored):
    points_by_person = {}
    unique_sprints_by_person = {}

    for issue in issues:
        sprints = issue['fields'][sprint]
        assignee = issue['fields']['assignee']

        if not assignee:
            continue

        display_name = assignee['displayName']

        # Skip if display_name is in the ignored list
        if display_name in ignored:
            continue

        story_points = issue['fields'][points]

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
