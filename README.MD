# Introduction

This is a collection (for, a collection of one) utilities to interact with Jira using Python. Each utility comes in the form of one script.

All scripts here will rely on a single file called 'credentials.json' in the following format:

```
{
   "key":"<YOURKEY>",
   "keyOwner": "KEY_EMAIL_ADDRESS",
   "assignee":"ASSIGNEE_EMAIL_ADDRESS",
   "project": "PROJECT KEY",
   "instance": "INSTANCE DOMAIN"
   "destinationFile": "FILE WHERE SPRINT ITEMS GO"
   "statuses": ["Status1", "Status2"]
}
```
As you can see, there are more than just 'credentials' here. Right now, there is an assumption that you are working with your own issues on a single Jira board. This might change down the road if I add additional scripts to this repository.

Note that the "instance" key requires only the domain names, ommitting https:// etc. (e.g. "instance.atlassian.net").

For details on getting your key and keyOwner details, check out Atlassian's [documentation][1].

## update_sprint_items_obs.py

This script queries sprint items for a given user and outputs them to a file, grouped under headings for their status. I use this primarily to update an md file that I reference on an Obsidian dashboard. 

Note that the statuses should match all of the statuses of the project that you are querying. The output will be based on the order that they are entered in the json above.

You'll also need to update the "destinationFile" key with the full path to the file you want to update. My recommendation is to give this file an .md extension as that's the format used, but it will render just fine as a txt file as well. 

[1]: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
