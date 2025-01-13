1. Brevo API:
The purpose of this project is to synchronize customer data, specifically when they install or uninstall our app, with Brevo. This allows our agents to follow up with them effectively.
- After receiving data through a webhook, I extract, clean, and transform it into normalized data.
![image](https://github.com/user-attachments/assets/d75ff9a3-2c29-4faf-94e7-69cdde62e71a)

-  The processed data is then inserted into Baserow and synchronized with the appropriate list on Brevo.
![image](https://github.com/user-attachments/assets/f5da9607-4ab0-42bb-b8dc-4c71c0390d25)

2. Affiliate Impact API:
In this project, I utilized three APIs from Affiliate Impact to generate individual reports:
 - Daily Metrics Report: This report provides daily summarized metrics pre-calculated by Impact.
![image](https://github.com/user-attachments/assets/4336dbce-75b3-4c76-9503-c378593c0a1d)

 - Detail Actions Report: Using the API, I extracted detailed actions such as Free Trial, Paid Trial, and Online Sale activities for each customer.
![image](https://github.com/user-attachments/assets/451d4ed2-dfc2-42ca-ae39-ddef9fe607af)

Detailed Clicks Report: Retrieving detailed click data was more complex, as it required a multi-step process. First, an API call returns another API endpoint to request the data. After initiating the request, a delay of approximately 30 seconds is needed before the data becomes available for download.
![image](https://github.com/user-attachments/assets/179c9211-eb38-4a3a-811c-3cf6236faa67)

