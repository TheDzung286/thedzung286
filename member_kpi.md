These are the flows that i use to receive data from Jira, transform and export to Gsheet.
1. Getting Data
![image](https://github.com/user-attachments/assets/90e7711c-474f-4a2b-a5fe-440cd1d17d39)

First, when an issue on Jira was updated, the data was sent to the webhook. I then searched the Project Issue table in Baserow to check if the issue already existed. If it did, I updated the existing record; if not, I created a new issue in Baserow.

Next, I queried several tables in Strapi to retrieve the indices for the assignee, reporter, and project. These indices were used to update the Project Issue table accordingly.

The similar flow was applied for Issue Worklog
![image](https://github.com/user-attachments/assets/d9f7ea24-aca9-402b-b06d-85fa58e56245)

However, The difference lies in tracking the first developer who logs into the issue, as they are designated as the main developer for the task. Any subsequent logins by other developers classify them as supporting developers or testers for the issue.

2. Transform data
![image](https://github.com/user-attachments/assets/77223f05-31da-4023-b86b-fb58b2faac3b)
After gathering all the necessary data, I need to transform it.

Since a developer may log multiple times for a single issue, I consolidate these entries into one record per log type (e.g., "Support," "Doing," or "ET") for each developer.

Each log type has a specific value, while each issue has its own estimate time and complexity. The task value is calculated as the product of these indices.
![image](https://github.com/user-attachments/assets/1fed049b-dea3-4055-a0bd-89c6839eb62c)

3. Export to Gsheet:
   I run this script to export to each file Google sheet (about 60 files for 60 members)
   https://github.com/TheDzung286/thedzung286/blob/main/export_kpi_for_each_menber
