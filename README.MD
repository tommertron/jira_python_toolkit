

## update_sprint_items_obs.py

This script queries sprint items for a given user and outputs them to a file, grouped under headings for their status. I use this primarily to update an md file that I reference on an Obsidian dashboard. 

This script replies on a json file called "credentials.json" existing in the same directory as the script run with the following format:

```
{
   "key":"<YOURKEY",
   "keyOwner": "KEY_EMAIL_ADDRESS",
   "assignee":"ASSIGNEE_EMAIL_ADDRESS",
   "project": "PROJECT KEY",
   "instance": "INSTANCE DOMAIN"
   "destinationFile": "FILE WHERE SPRINT ITEMS GO"
}
```

