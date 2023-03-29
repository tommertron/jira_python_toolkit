# Introduction

This is a collection of utilities to interact with Jira using Python. Each utility comes in the form of one script.

Most scripts here will default to returning or printing out some basic statistics in plain text Markdown format.

## Credentials
All scripts here will rely on a single file called 'credentials.json' in the following format:

```
{
   "key":"<YOURKEY>",
   "keyOwner": "KEY_EMAIL_ADDRESS",
   "assignee":"ASSIGNEE_EMAIL_ADDRESS",
   "instance": "INSTANCE DOMAIN"
}
```

Note that the "instance" key requires only the domain names, ommitting https:// etc. (e.g. "instance.atlassian.net").

For details on getting your key and keyOwner details, check out Atlassian's [documentation][1].

## Settings

Most scripts will also reference a 'settings.json' file in the following format:

```
{
   "project": "IT",
   "destinationFile": "FILE WHERE SPRINT ITEMS GO"
   "statuses": ["Status1", "Status2"]
   "epics": ["KEY-2", "KEY-4","KEY-1","KEY-5"],
   "ignored_people": ["John Doe", "Jane Doe"],
   "labels": ["label_one","label_two"],
   "points": "customfield_xxxxx", 
   "sprint": "customfield_xxxxx"
}
```

The 'points' and 'sprint' fields need to be defined per instance, as for some reason Jira says that these are custom fields, even though they are standard fields out of the box with most projects. 🤷‍♂️

## update_sprint_items_obs.py

This script queries sprint items for a given user and outputs them to a file, grouped under headings for their status. I use this primarily to update an md file that I reference on an Obsidian dashboard. 

Note that the statuses should match all of the statuses of the project that you are querying. The output will be based on the order that they are entered in the json above.

You'll also need to update the "destinationFile" key with the full path to the file you want to update. My recommendation is to give this file an .md extension as that's the format used, but it will render just fine as a txt file as well. 


## sprint_point_calculator.py

Not very Agile! But if you really want to know, it will give you how many points, on average, each person has completed over all sprints in the given project.

Reads the projects and ignored people from the settings.json file.

## epic_calculator.py

Reads a set of epics as defined in the epics calculator and gives you a percentage done and how many issues are in the epic. 


[1]: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
